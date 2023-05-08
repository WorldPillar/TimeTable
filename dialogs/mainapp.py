import os
from functools import partial

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from dialogs.listdialog import ListDialog
from ioprocessors.excelprocessor import ExcelProcessor
from ioprocessors.jsonporcessor import JSONProcessor
from schooldata.data import SchoolData
from schooldata.extendedRS import ExtendedRecursiveSwapping
from schooldata.school import School
from schooldata.validateData import Validator
from windows import mainWindow, schoolWindow
from dialogs.widgets.listWidget import MyListWidget

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
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

    def create_table(self, days_amount: int = 5, lessons_amount: int = 6):
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

    def _create_days_table(self, days_amount: int = 5, lessons_amount: int = 6):
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

    def set_save_actions(self):
        menu = QtWidgets.QMenu()
        menu.addAction(QIcon('icons/savefileicon.svg'), 'Сохранить', self.save_file)
        menu.addAction(QIcon('icons/saveasfileicon.svg'), 'Сохранить как', self.save_as_file)
        self.tbtn_save.setMenu(menu)
        return

    def set_export_actions(self):
        menu = QtWidgets.QMenu()
        menu.addAction(QIcon('icons/classicon.svg'), 'Экспорт расписания классов', self.export_class_table)
        menu.addAction(QIcon('icons/teachericon.svg'), 'Экспорт расписания учителей', self.export_teacher_table)
        self.tbtn_export.setMenu(menu)
        return

    def new_file(self):
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

    def open_file(self):
        (file_name, _) = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть", desktop, "*.sked")
        if file_name != '':
            try:
                self.school = JSONProcessor.json_read(file_name)
            finally:
                self.set_buttons_available()
                self.create_table(self.school.amount_days, self.school.amount_lessons)
                self.unallocated_list.add_unallocated_lessons(self.school.unallocated)
                self.tableWidget_timetable.fill_table(self.school)
        self.file_path = file_name
        return

    def save_file(self):
        if self.file_path == '':
            self.save_as_file()
        else:
            try:
                JSONProcessor.json_save(self.file_path, self.school)
            except NotADirectoryError:
                print('error dir')
        return

    def save_as_file(self):
        rout = desktop
        if self.file_path != '':
            rout = self.file_path

        (file_name, _) = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить как", rout, "*.sked")
        if file_name != '':
            try:
                JSONProcessor.json_save(file_name, self.school)
            except NotADirectoryError:
                print('error dir')

        self.file_path = file_name
        return

    def export_class_table(self):
        self.export_table('class')
        return

    def export_teacher_table(self):
        self.export_table('teacher')
        return

    def export_table(self, param):
        rout = desktop
        if self.table_file_path != '':
            rout = self.table_file_path

        (file_name, _) = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить как", rout, "*.xlsx")
        if file_name != '':
            try:
                if not ExcelProcessor.export_table(self.school, param, file_name):
                    errorbox = QtWidgets.QMessageBox(self)
                    errorbox.setWindowTitle('Ошибка')
                    errorbox.setText('Закройте excel файл перед сохранением')
                    errorbox.exec()
            except NotADirectoryError:
                print('error dir')

        self.table_file_path = file_name
        return

    def input_lists_window(self, value: int):
        dlg = ListDialog(self, self.school)
        dlg.tabWidget.setCurrentIndex(value)
        dlg.exec()
        self.tableWidget_timetable.fill_table(self.school)
        self.unallocated_list.add_unallocated_lessons(self.school.unallocated)
        return

    def scheduling(self):
        """
        Функция вызова алгоритма составления расписания. После составления вызывает метод заполнения таблицы.
        """
        conflicts = Validator.validate(self.school)
        if len(conflicts) != 0:
            comments = ''
            for comment in conflicts:
                comments = comments + comment + '\n' + '\n'

            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle('Ошибки')
            msg.setText(comments)
            msg.exec()
            return

        self.school.drop_current_time()
        builder = ExtendedRecursiveSwapping(self.school)
        self.school = builder.start()
        self.tableWidget_timetable.fill_table(self.school)

        self.unallocated_list.add_unallocated_lessons(self.school.unallocated)
        if len(self.school.unallocated) > 0:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle('Неудача')
            msg.setText(f'Не распределено {len(self.school.unallocated)} уроков.\n'
                        f'Они были помещены в список внизу окна.')
            msg.exec()
        return

    def set_buttons_available(self):
        self.tbtn_save.setDisabled(False)
        self.tbtn_export.setDisabled(False)
        self.tbtn_subject.setDisabled(False)
        self.tbtn_class.setDisabled(False)
        self.tbtn_teacher.setDisabled(False)
        self.tbtn_lesson.setDisabled(False)
        self.tbtn_scheduling.setDisabled(False)
        return


class SchoolDialog(QtWidgets.QDialog, schoolWindow.Ui_dialogSchool):
    def __init__(self, parent):
        super(SchoolDialog, self).__init__(parent)
        self.setupUi(self)

        self.amount_lessons_combobox.addItems(SchoolData.max_lessons_in_day)
        self.amount_lessons_combobox.setCurrentIndex(7)
        self.amount_lessons_combobox.setFixedWidth(60)

        self.amount_days_combobox.addItems(SchoolData.get_days_positions())
        self.amount_days_combobox.setCurrentIndex(4)
        self.amount_days_combobox.setFixedWidth(60)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)
