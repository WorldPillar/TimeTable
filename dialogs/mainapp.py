import logging
import os
import time
from functools import partial

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from dialogs.inputdialogs import SchoolDialog
from dialogs.listdialog import ListDialog
from windows import mainWindow
from dialogs.widgets.listWidget import MyListWidget
from dialogs.widgets.messageBox import showMessage
from ioprocessors.excelprocessor import ExcelProcessor
from ioprocessors.jsonprocessor import JSONProcessor
from schooldata.data import SchoolData
from schooldata.extendedRS import ExtendedRecursiveSwapping
from schooldata.school import School
from schooldata.validateData import Validator

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    """
    Главное окно программы
    """

    def __init__(self):
        super().__init__()
        self.school = None
        self.setupUi(self)
        self.setWindowIcon(QIcon('icons/schoolicon.svg'))
        self.file_path = ''
        self.table_file_path = ''

        self.tbtn_newfile.clicked.connect(self.new_file)
        self.tbtn_open.clicked.connect(self.open_file)

        self.tbtn_subject.clicked.connect(partial(self.input_lists_window, 0))
        self.tbtn_class.clicked.connect(partial(self.input_lists_window, 1))
        self.tbtn_teacher.clicked.connect(partial(self.input_lists_window, 2))
        self.tbtn_lesson.clicked.connect(partial(self.input_lists_window, 3))

        self.tbtn_scheduling.clicked.connect(self.scheduling)
        self.set_save_actions()
        self.set_export_actions()
        self.create_table()

        self.unallocated_list = MyListWidget(self, self.tableWidget_timetable)
        self.verticalLayout_2.addWidget(self.unallocated_list)
        self.tableWidget_timetable.unallocated_list = self.unallocated_list

    def create_table(self, days_amount: int = 5, lessons_amount: int = 6) -> None:
        """
        Вызов функций для создания заголовков таблиц. Вызывать функцию только при обновлении параметров школы.
        :param days_amount: количество учебных дней в неделю.
        :param lessons_amount: максимальное количество учебных уроков в день.
        """
        # Вызов функции для таблицы с днями недели
        self._create_days_table(days_amount, lessons_amount)
        # Вызов функции для таблицы с позициями уроков
        self.tableWidget_timetable.create_table(days_amount, lessons_amount)
        return

    def _create_days_table(self, days_amount: int = 5, lessons_amount: int = 6) -> None:
        """
        Метод создаёт таблицу дней как заголовок общей таблицы.
        :param days_amount: Количество дней в рабочей неделе.
        :param lessons_amount: Количество уроков в день.
        """
        self.tableWidget_days.setRowCount(0)
        self.tableWidget_days.setFixedHeight(15)
        self.tableWidget_days.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.tableWidget_days.setColumnCount(days_amount * lessons_amount)
        self.tableWidget_days.setRowCount(1)

        for i in range(days_amount):
            position = i * lessons_amount
            self.tableWidget_days.setSpan(0, position, 1, lessons_amount)
            item = QtWidgets.QTableWidgetItem(SchoolData.get_day_name(i))
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.tableWidget_days.setItem(0, position, item)

        self.tableWidget_days.verticalHeader().setMinimumSize(31, 0)
        self.tableWidget_days.setVerticalHeaderLabels([''])

        self.tableWidget_days.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        return

    def set_save_actions(self) -> None:
        """
        Метод добавляет действия для кнопки "Сохранить".
        """
        menu = QtWidgets.QMenu()
        menu.addAction(QIcon('icons/savefileicon.svg'), 'Сохранить', self.save_file)
        menu.addAction(QIcon('icons/saveasfileicon.svg'), 'Сохранить как', self.save_as_file)
        self.tbtn_save.setMenu(menu)
        return

    def set_export_actions(self) -> None:
        """
        Метод добавляет действия для кнопки "Экспорт".
        """
        menu = QtWidgets.QMenu()
        menu.addAction(QIcon('icons/classicon.svg'), 'Экспорт расписания классов', self.export_class_table)
        menu.addAction(QIcon('icons/teachericon.svg'), 'Экспорт расписания учителей', self.export_teacher_table)
        self.tbtn_export.setMenu(menu)
        return

    def new_file(self) -> None:
        """
        Метод создания нового файла. Создаётся объект класса School.
        """
        dlg = SchoolDialog(self)
        if dlg.exec():
            name = dlg.name_lineEdit.text()
            lessons = dlg.amount_lessons_combobox.currentIndex()
            days = dlg.amount_days_combobox.currentIndex()
            lessons = int(SchoolData.max_lessons_in_day[lessons])
            days = int(SchoolData.days[days]["Position"])
            self.school = School(name, days, lessons)

            self.set_buttons_available()
            self.create_table(days, lessons)
            self.unallocated_list.clear()

        self.file_path = ''
        return

    def open_file(self) -> None:
        """
        Метод открытия файла.
        """
        (file_name, _) = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть", desktop, "*.sked")
        if file_name != '':
            try:
                self.school = JSONProcessor.json_read(file_name)
                self.set_buttons_available()
                self.create_table(self.school.amount_days, self.school.amount_lessons)
                self.unallocated_list.add_unallocated_lessons(self.school.unallocated)
                self.tableWidget_timetable.fill_table(self.school)
            except BaseException:
                logging.error('PARSE_FILE_ERROR')
                showMessage(title='Ошибка', message='Не получилось открыть файл')
        self.file_path = file_name
        return

    def save_file(self) -> None:
        """
        Метод сохранения файла с известным путём.
        """
        if self.file_path == '':
            self.save_as_file()
        else:
            self.save()
        return

    def save_as_file(self) -> None:
        """
        Метод сохранения файла без известного пути.
        """
        rout = desktop
        if self.file_path != '':
            rout = self.file_path

        (file_name, _) = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить как", rout, "*.sked")
        self.file_path = file_name
        if self.file_path != '':
            self.save()
        return

    def save(self):
        try:
            JSONProcessor.json_save(self.file_path, self.school)
        except BaseException:
            logging.error('SAVE_ERROR')
            showMessage(title='Ошибка', message='Не получилось сохранить файл')
        return

    def export_class_table(self) -> None:
        self.export_table('class')
        return

    def export_teacher_table(self) -> None:
        self.export_table('teacher')
        return

    def export_table(self, param: str) -> None:
        """
        Метод экспортирования таблицы расписания в excel.
        :param param: Экспорт расписания учителей при значении 'teacher'. Экспорт расписания классов при 'class'.
        """
        rout = desktop
        if self.table_file_path != '':
            rout = self.table_file_path

        (file_name, _) = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить как", rout, "*.xlsx")
        if file_name != '':
            try:
                ExcelProcessor.export_table(self.school, param, file_name)
            except IOError:
                logging.error('EXCEL_IOERROR')
                showMessage(title='Ошибка', message='Не удалось экспортировать excel файл')

        self.table_file_path = file_name
        return

    def input_lists_window(self, value: int) -> None:
        """
        Метод открывает диалоговое окно заполнения список школы.
        :param value: Начальная вкладка при открытии окна.
        """
        dlg = ListDialog(self, self.school)
        dlg.tabWidget.setCurrentIndex(value)
        dlg.exec()
        self.tableWidget_timetable.fill_table(self.school)
        self.unallocated_list.add_unallocated_lessons(self.school.unallocated)
        return

    def scheduling(self) -> None:
        """
        Метод вызова алгоритма составления расписания. После составления вызывает метод заполнения таблицы.
        """
        conflicts = Validator.validate(self.school)
        if len(conflicts) != 0:
            comments = ''
            for comment in conflicts:
                comments = comments + comment + '\n' + '\n'
            showMessage(title='Ошибки', message=comments)
            return

        self.school.drop_current_time()
        builder = ExtendedRecursiveSwapping(self.school)

        start = time.time()
        self.school = builder.start()
        end = time.time()

        self.tableWidget_timetable.fill_table(self.school)
        self.unallocated_list.add_unallocated_lessons(self.school.unallocated)

        message = 'Время работы: ' + time.strftime("%H:%M:%S", time.gmtime(end - start)) + '\n' \
                  + 'Нераспределенно уроков: ' +\
                  f'{len(self.school.unallocated)}\n'

        showMessage(title='Расписание составлено', message=message)
        return

    def set_buttons_available(self) -> None:
        self.tbtn_save.setDisabled(False)
        self.tbtn_export.setDisabled(False)
        self.tbtn_subject.setDisabled(False)
        self.tbtn_class.setDisabled(False)
        self.tbtn_teacher.setDisabled(False)
        self.tbtn_lesson.setDisabled(False)
        self.tbtn_scheduling.setDisabled(False)
        return
