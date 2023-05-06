from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QDialogButtonBox

from schooldata.data import SchoolData
from schooldata.school import School, Subject, StudentClass, Teacher, Lesson
from windows import subjectWindow, classWindow, teacherWindow, lessonWindow, worktimeWindow


class SubjectDialog(QDialog, subjectWindow.Ui_dialogSubject):
    def __init__(self, parent, subject: Subject = None):
        super(SubjectDialog, self).__init__(parent)
        self.setupUi(self)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        self.name_lineEdit.textChanged.connect(self.abb_constructor)
        if subject is not None:
            self.name_lineEdit.setText(subject.name)
            self.abb_lineEdit.setText(subject.abbreviation)

    def abb_constructor(self):
        words = list(filter(None, self.name_lineEdit.text().split(' ')))

        abb = ''
        if len(words) == 1:
            abb = words[0][:3]
        elif len(words) > 1:
            for word in words:
                abb += f'{word[0]}'
        self.abb_lineEdit.setText(abb)
        return

    def accept(self) -> None:
        if self.name_lineEdit.text():
            if self.abb_lineEdit.text() == '':
                self.abb_constructor()
            super().accept()
        return


class ClassDialog(QDialog, classWindow.Ui_dialogClass):
    def __init__(self, parent, student_class: StudentClass = None):
        super(ClassDialog, self).__init__(parent)
        self.setupUi(self)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        self.name_lineEdit.textChanged.connect(self.abb_constructor)
        if student_class is not None:
            self.name_lineEdit.setText(student_class.name)
            self.abb_lineEdit.setText(student_class.abbreviation)

    def abb_constructor(self):
        words = list(filter(None, self.name_lineEdit.text().split(' ')))

        abb = ''
        if len(words) == 1:
            abb = words[0]
        elif len(words) > 1:
            for word in words:
                abb += f'{word[:3]}.'
        self.abb_lineEdit.setText(abb)
        return

    def accept(self) -> None:
        if self.name_lineEdit.text():
            if self.abb_lineEdit.text() == '':
                self.abb_constructor()
            super().accept()
        return


class TeacherDialog(QDialog, teacherWindow.Ui_dialogTeacher):
    def __init__(self, parent, teacher: Teacher = None):
        super(TeacherDialog, self).__init__(parent)
        self.setupUi(self)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        self.family_lineEdit.textChanged.connect(self.abb_constructor)
        self.name_lineEdit.textChanged.connect(self.abb_constructor)
        if teacher is not None:
            self.family_lineEdit.setText(teacher.family)
            self.name_lineEdit.setText(teacher.name)
            self.abb_lineEdit.setText(teacher.abbreviation)
            self.workload_lineEdit.setText(str(teacher.workload or ''))

    def abb_constructor(self):
        family = self.family_lineEdit.text()
        name = self.name_lineEdit.text()

        abb = f'{name[:1]}{family[:1]}'
        self.abb_lineEdit.setText(abb)
        return

    def accept(self) -> None:
        if self.family_lineEdit.text():
            if self.abb_lineEdit.text() == '':
                self.abb_constructor()
            super().accept()
        return


class LessonDialog(QDialog, lessonWindow.Ui_dialogLesson):
    def __init__(self, parent, school: School, lesson: Lesson = None):
        super(LessonDialog, self).__init__(parent)
        self.setupUi(self)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        self.school = school
        self.fill_combobox()
        if lesson is not None:
            self.teacher_combobox.setCurrentIndex(lesson.teacher.id)
            self.class_combobox.setCurrentIndex(lesson.student_class.id)
            self.subject_combobox.setCurrentIndex(lesson.subject.id)
            self.count_combobox.setCurrentIndex(lesson.amount - 1)

    def fill_combobox(self):
        self.teacher_combobox.addItems([x.get_string() for x in self.school.teachers])
        self.teacher_combobox.setCurrentIndex(-1)
        self.class_combobox.addItems([x.get_string() for x in self.school.student_classes])
        self.class_combobox.setCurrentIndex(-1)
        self.subject_combobox.addItems([x.get_string() for x in self.school.subjects])
        self.subject_combobox.setCurrentIndex(-1)
        self.count_combobox.addItems(SchoolData.get_max_lesson_in_week(self.school.amount_days))
        self.count_combobox.setCurrentIndex(-1)

    def accept(self) -> None:
        if (self.teacher_combobox.currentIndex() == -1) or (self.class_combobox.currentIndex() == -1) or \
                (self.subject_combobox.currentIndex() == -1) or (self.count_combobox.currentIndex() == -1):
            return
        super().accept()


class WorkTimeDialog(QDialog, worktimeWindow.Ui_WorkTimeDialog):
    def __init__(self, parent, item):
        super(WorkTimeDialog, self).__init__(parent)
        self.setupUi(self)
        self.item = item
        self.tableWidget.itemClicked.connect(self.item_clicked)
        self.set_tables()

    def set_tables(self):
        self.tableWidget.setColumnCount(len(self.item.worktime[0]))
        self.tableWidget.setRowCount(len(self.item.worktime))

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.tableWidget.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.tableWidget.setVerticalHeaderLabels(SchoolData.get_days_abb())

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for day in range(len(self.item.worktime)):
            for les_pos in range(len(self.item.worktime[day])):
                self.tableWidget.setItem(day, les_pos, WorkTimeItem(self.item.worktime[day][les_pos]))
        return

    def item_clicked(self):
        (row, col) = (self.tableWidget.selectedItems()[0].row(), self.tableWidget.selectedItems()[0].column())
        self.tableWidget.item(row, col).reverse()

        palette = self.tableWidget.palette()
        if self.tableWidget.item(row, col).is_available:
            color = QtGui.QColor(0, 204, 0)
        else:
            color = QtGui.QColor(204, 0, 0)
        palette.setBrush(QtGui.QPalette.ColorRole.Highlight, QtGui.QBrush(color))
        self.tableWidget.setPalette(palette)

    def accept(self) -> None:
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.item.worktime[i][j] = self.tableWidget.item(i, j).is_available
        super().accept()


class WorkTimeItem(QTableWidgetItem):
    def __init__(self, available: int):
        super().__init__('')
        self.is_available = available
        self._draw()

    def reverse(self):
        self.is_available -= 1
        self.is_available *= -1
        self._draw()

    def _draw(self):
        if self.is_available == 1:
            self.setBackground(QtGui.QColor(0, 204, 0))
        else:
            self.setBackground(QtGui.QColor(204, 0, 0))
