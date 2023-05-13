from copy import copy, deepcopy

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem

from dialogs.inputdialogs import LessonDialog
from schooldata.data import SchoolData
from schooldata.school import School, Lesson
from windows import tab


class LessonTab(QtWidgets.QTabWidget, tab.Ui_Form):
    def __init__(self, school: School, headers: [str]):
        super(LessonTab, self).__init__()
        self.setupUi(self)
        self.headers = headers
        self.school = school

        self.add_spacer()
        self.set_table()

        self.tableWidget.selectionModel().selectionChanged.connect(self.change_btn_state)
        self.btn_new.clicked.connect(self.new)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_delete.clicked.connect(self.delete)

    def add_spacer(self):
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        return

    def change_btn_state(self):
        if self.tableWidget.selectedItems():
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)
        else:
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
        return

    def insert_row(self, table, new_obj):
        rowcount = table.rowCount()
        table.insertRow(rowcount)
        self.update_row(table, new_obj, rowcount)

    def update_row(self, table, new_obj, row):
        i = 0
        for attribute in new_obj.get_attributes():
            table.setItem(row, i, QTableWidgetItem(str(attribute or '')))
            i += 1

    def set_table(self):
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setRowCount(len(self.school.lessons))

        for row in range(self.tableWidget.rowCount()):
            self.update_row(self.tableWidget, self.school.lessons[row], row)
        return

    def new(self):
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
                lesson.teacher.append(secondTeacher)

            self.school.update_lesson_amount(lesson, 0)

            self.insert_row(self.tableWidget, lesson)

        self.tableWidget.clearSelection()
        return

    def edit(self):
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
            old_teachers = deepcopy(lesson.teacher)
            old_subject = deepcopy(lesson.subject)
            old_class = deepcopy(lesson.student_class)

            lesson.update_lesson_data(subject, teachers, student_class, amount, duration)
            self.school.validate_lesson_by_old(lesson, old_subject, old_class, old_teachers,
                                               old_amount, old_duration)

            self.update_row(self.tableWidget, lesson, position)
        return

    def delete(self):
        position = self.tableWidget.selectedItems()[0].row()
        self.tableWidget.removeRow(position)
        self.school.pop_lesson(position)

        self.tableWidget.clearSelection()
        return
