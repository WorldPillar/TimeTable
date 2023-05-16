from copy import copy, deepcopy

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem

from dialogs.inputdialogs import LessonDialog
from schooldata.data import SchoolData
from schooldata.school import School, Lesson
from windows import tab


class LessonTab(QtWidgets.QTabWidget, tab.Ui_Form):
    """
    Класс вкладки "Уроки" списков школы
    """

    def __init__(self, school: School, headers: [str]):
        super(LessonTab, self).__init__()
        self.setupUi(self)
        self.headers = headers
        self.school = school

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.set_table()

        self.tableWidget.selectionModel().selectionChanged.connect(self.change_btn_state)
        self.btn_new.clicked.connect(self._new)
        self.btn_edit.clicked.connect(self._edit)
        self.btn_delete.clicked.connect(self._delete)

    def change_btn_state(self) -> None:
        """
        Метод изменяет состояние кнопок.
        """
        if self.tableWidget.selectedItems():
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)
        else:
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
        return

    def insert_row(self, table, new_obj) -> None:
        """
        Добавляет новую строчку в таблицу.
        :param table: Таблица, в которую добавляется строчка.
        :param new_obj: Объект, который помещается в таблицу.
        """
        rowcount = table.rowCount()
        table.insertRow(rowcount)
        self.update_row(table, new_obj, rowcount)

    @staticmethod
    def update_row(table, new_obj, row) -> None:
        """
        Обновление информации в строчке таблицы.
        :param table: Таблица, в которой обновляется информация.
        :param new_obj: Объект, на основе которого обновится информация.
        :param row: Строчка, информацию которой необходимо обновить.
        """
        i = 0
        for attribute in new_obj.get_attributes():
            table.setItem(row, i, QTableWidgetItem(str(attribute or '')))
            i += 1

    def set_table(self) -> None:
        """
        Создание таблицы.
        """
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setRowCount(len(self.school.lessons))

        for row in range(self.tableWidget.rowCount()):
            self.update_row(self.tableWidget, self.school.lessons[row], row)
        return

    def _new(self) -> None:
        """
        Метод создания нового объекта.
        """
        dlg = LessonDialog(self, self.school)
        if dlg.exec():
            teacher = self.school.teachers[dlg.teacher_combobox.currentIndex()]
            subject = self.school.subjects[dlg.subject_combobox.currentIndex()]
            student_class = self.school.student_classes[dlg.class_combobox.currentIndex()]
            amount = int(SchoolData.get_max_lesson_in_week(self.school.amount_days)[dlg.count_combobox.currentIndex()])
            duration = dlg.duration_combobox.currentIndex() + 1
            lesson = Lesson(subject, teacher, student_class, amount, duration)
            self.school.lessons.append(lesson)

            if dlg.secondTeacherCombobox is not None:
                secondTeacher = self.school.teachers[dlg.secondTeacherCombobox.currentIndex()]
                lesson.teachers.append(secondTeacher)

            self.school.update_lesson_amount(lesson, 0)

            self.insert_row(self.tableWidget, lesson)

        self.tableWidget.clearSelection()
        return

    def _edit(self) -> None:
        """
        Метод редактирования информации выбранного объекта таблицы.
        """
        position = self.tableWidget.selectedItems()[0].row()
        lesson = self.school.lessons[position]
        dlg = LessonDialog(self, self.school, lesson)
        if dlg.exec():
            teachers = [self.school.teachers[dlg.teacher_combobox.currentIndex()]]
            if dlg.secondTeacherCombobox is not None:
                secondTeacher = self.school.teachers[dlg.secondTeacherCombobox.currentIndex()]
                teachers.append(secondTeacher)
            subject = self.school.subjects[dlg.subject_combobox.currentIndex()]
            student_class = self.school.student_classes[dlg.class_combobox.currentIndex()]
            amount = int(SchoolData.get_max_lesson_in_week(self.school.amount_days)[dlg.count_combobox.currentIndex()])
            duration = dlg.duration_combobox.currentIndex() + 1

            old_amount = lesson.amount
            old_duration = lesson.duration
            old_teachers = deepcopy(lesson.teachers)
            old_subject = deepcopy(lesson.subject)
            old_class = deepcopy(lesson.student_class)

            lesson.update_lesson_data(subject, teachers, student_class, amount, duration)
            self.school.validate_lesson_by_old(lesson, old_subject, old_class, old_teachers,
                                               old_amount, old_duration)

            self.update_row(self.tableWidget, lesson, position)
        return

    def _delete(self) -> None:
        """
        Метод удаления выбранного объекта таблицы.
        """
        position = self.tableWidget.selectedItems()[0].row()
        self.tableWidget.removeRow(position)
        self.school.pop_lesson(position)

        self.tableWidget.clearSelection()
        return
