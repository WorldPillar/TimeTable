from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView,\
    QDialogButtonBox, QPushButton, QComboBox, QMessageBox

from schooldata.data import SchoolData
from schooldata.school import School, Subject, StudentClass, Teacher, Lesson
from windows import subjectWindow, classWindow, teacherWindow, lessonWindow, worktimeWindow, schoolWindow


def showMessage(message: str = 'Заполните все необходимые поля'):
    msg = QMessageBox()
    msg.setWindowTitle('Ошибка')
    msg.setText(message)
    msg.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
    msg.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
    msg.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)
    msg.exec()


class SchoolDialog(QDialog, schoolWindow.Ui_dialogSchool):
    """
    Диалоговое окно ввода информации о школе.
    """

    def __init__(self, parent):
        super(SchoolDialog, self).__init__(parent)
        self.setupUi(self)

        self.amount_lessons_combobox.addItems(SchoolData.max_lessons_in_day)
        self.amount_lessons_combobox.setCurrentIndex(7)
        self.amount_lessons_combobox.setFixedWidth(60)

        self.amount_days_combobox.addItems(SchoolData.get_days_positions())
        self.amount_days_combobox.setCurrentIndex(4)
        self.amount_days_combobox.setFixedWidth(60)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)


class SubjectDialog(QDialog, subjectWindow.Ui_dialogSubject):
    """
    Диалоговое окно ввода информации о предмете.
    """

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
        # Заполняем поля, если предмет редактируется
        if subject is not None:
            self.name_lineEdit.setText(subject.name)
            self.abb_lineEdit.setText(subject.abbreviation)

    def abb_constructor(self) -> None:
        """
        Метод генерации сокращения названия.
        """
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
        """
        Проверка заполненности полей. Если необходимые поля не заполнены, высвечивается ошибка.
        """
        if self.name_lineEdit.text():
            if self.abb_lineEdit.text() == '':
                self.abb_constructor()
            super().accept()
        else:
            showMessage()
        return


class ClassDialog(QDialog, classWindow.Ui_dialogClass):
    """
    Диалоговое окно ввода информации о классе.
    """

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
        # Заполняем поля, если класс редактируется
        if student_class is not None:
            self.name_lineEdit.setText(student_class.name)
            self.abb_lineEdit.setText(student_class.abbreviation)

    def abb_constructor(self) -> None:
        """
        Метод генерации сокращения названия.
        """
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
        """
        Проверка заполненности полей. Если необходимые поля не заполнены, высвечивается ошибка.
        """
        if self.name_lineEdit.text():
            if self.abb_lineEdit.text() == '':
                self.abb_constructor()
            super().accept()
        else:
            showMessage()
        return


class TeacherDialog(QDialog, teacherWindow.Ui_dialogTeacher):
    """
    Диалоговое окно ввода информации об учителе.
    """

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
        # Заполняем поля, если учитель редактируется
        if teacher is not None:
            self.family_lineEdit.setText(teacher.family)
            self.name_lineEdit.setText(teacher.name)
            self.abb_lineEdit.setText(teacher.abbreviation)
            self.workload_lineEdit.setText(str(teacher.workload or ''))

    def abb_constructor(self) -> None:
        """
        Метод генерации сокращения названия.
        """
        family = self.family_lineEdit.text()
        name = self.name_lineEdit.text()

        abb = f'{name[:1]}{family[:1]}'
        self.abb_lineEdit.setText(abb)
        return

    def accept(self) -> None:
        """
        Проверка заполненности полей. Если необходимые поля не заполнены, высвечивается ошибка.
        """
        if self.family_lineEdit.text() and self.name_lineEdit.text():
            if self.abb_lineEdit.text() == '':
                self.abb_constructor()
            super().accept()
        else:
            showMessage()
        return


class LessonDialog(QDialog, lessonWindow.Ui_dialogLesson):
    """
    Диалоговое окно ввода информации об уроке.
    """

    def __init__(self, parent, school: School, lesson: Lesson = None):
        super(LessonDialog, self).__init__(parent)
        self.setupUi(self)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText('Ок')
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отменить')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        self.deleteButton = QPushButton('Удалить')
        self.deleteButton.clicked.connect(self.pushButtonAdd)
        self.gridLayout_2.addWidget(self.deleteButton, 3, 1)

        self.secondTeacherCombobox: QComboBox = None
        self.pushButtonAdd()

        self.school = school
        self.fill_combobox()
        # Заполняем поля, если урок редактируется
        if lesson is not None:
            self.teacher_combobox.setCurrentIndex(lesson.teachers[0].id)
            if len(lesson.teachers) == 2:
                self.putCombobox(lesson.teachers[1].id)

            self.class_combobox.setCurrentIndex(lesson.student_class.id)
            self.subject_combobox.setCurrentIndex(lesson.subject.id)
            self.count_combobox.setCurrentIndex(lesson.amount - 1)
            self.duration_combobox.setCurrentIndex(lesson.duration - 1)

    def pushButtonAdd(self) -> QPushButton:
        """
        Метод добавляет кнопку Добавить.
        """
        buttonAdd = QPushButton('Добавить')
        buttonAdd.clicked.connect(self.addCombobox)
        self.secondTeacherCombobox = None

        self.gridLayout_2.addWidget(buttonAdd, 2, 1)
        self.gridLayout_2.itemAtPosition(3, 1).widget().hide()
        return buttonAdd

    def addCombobox(self) -> None:
        """
        Метод связывает событие нажатия кнопки Добавить и putCombobox.
        """
        self.putCombobox(-1)
        return

    def putCombobox(self, teacherId: int = -1) -> None:
        """
        Метод добавляет combobox для второго учителя
        """
        self.secondTeacherCombobox = QComboBox()
        self.secondTeacherCombobox.addItems([x.get_full_name() for x in self.school.teachers])
        self.secondTeacherCombobox.setCurrentIndex(teacherId)
        self.gridLayout_2.itemAtPosition(3, 1).widget().show()

        self.gridLayout_2.addWidget(self.secondTeacherCombobox, 2, 1)
        return

    def fill_combobox(self) -> None:
        """
        Метод заполняет поля урока.
        """
        self.teacher_combobox.addItems([x.get_full_name() for x in self.school.teachers])
        self.teacher_combobox.setCurrentIndex(-1)
        self.class_combobox.addItems([x.get_full_name() for x in self.school.student_classes])
        self.class_combobox.setCurrentIndex(-1)
        self.subject_combobox.addItems([x.get_full_name() for x in self.school.subjects])
        self.subject_combobox.setCurrentIndex(-1)
        self.count_combobox.addItems(SchoolData.get_max_lesson_in_week(self.school.amount_days))
        self.count_combobox.setCurrentIndex(-1)
        self.duration_combobox.addItems(['1', '2'])
        self.duration_combobox.setCurrentIndex(-1)
        return

    def accept(self) -> None:
        """
        Проверка заполненности полей и уникальности данных.
        Если поля не заполнены, либо совпадают учителя, то высвечивается ошибка.
        """
        if (self.teacher_combobox.currentIndex() == -1) or (self.class_combobox.currentIndex() == -1) or \
                (self.subject_combobox.currentIndex() == -1) or (self.count_combobox.currentIndex() == -1):
            showMessage()
            return
        if self.secondTeacherCombobox is not None:
            if self.teacher_combobox.currentIndex() == self.secondTeacherCombobox.currentIndex():
                showMessage('Учителя не могут быть одинаковыми')
                return
            if self.secondTeacherCombobox.currentIndex() == -1:
                showMessage()
                return
        super().accept()
        return


class WorkTimeDialog(QDialog, worktimeWindow.Ui_WorkTimeDialog):
    """
    Диалоговое окно редактирования рабочей недели.
    """

    def __init__(self, parent, item):
        super(WorkTimeDialog, self).__init__(parent)
        self.setupUi(self)
        self.item = item
        self.tableWidget.itemClicked.connect(self.item_clicked)
        self.set_tables()

    def set_tables(self) -> None:
        """
        Начальная отрисовка таблицы.
        """
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

    def item_clicked(self) -> None:
        """
        Событие, вызываемое при нажатии на ячейку. Изменяет её состояние на противоположное.
        """
        (row, col) = (self.tableWidget.selectedItems()[0].row(), self.tableWidget.selectedItems()[0].column())
        self.tableWidget.item(row, col).reverse()

        palette = self.tableWidget.palette()
        if self.tableWidget.item(row, col).is_available:
            color = QtGui.QColor(0, 204, 0)
        else:
            color = QtGui.QColor(204, 0, 0)
        palette.setBrush(QtGui.QPalette.ColorRole.Highlight, QtGui.QBrush(color))
        self.tableWidget.setPalette(palette)
        return

    def accept(self) -> None:
        """
        Метод, заполняющий таблицу рабочей недели для объекта на основе отредактированной таблицы self.tableWidget.
        """
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.item.worktime[i][j] = self.tableWidget.item(i, j).is_available
        super().accept()
        return


class WorkTimeItem(QTableWidgetItem):
    """
    Класс ячейки таблицы в WorkTimeDialog
    """

    def __init__(self, available: int):
        super().__init__('')
        self.is_available = available
        self._draw()

    def reverse(self) -> None:
        """
        Метод инвертирует значение self.is_available
        """
        self.is_available -= 1
        self.is_available *= -1
        self._draw()
        return

    def _draw(self) -> None:
        """
        Метод меняет цвет по значению self.is_available
        """
        if self.is_available == 1:
            self.setBackground(QtGui.QColor(0, 204, 0))
        else:
            self.setBackground(QtGui.QColor(204, 0, 0))
        return
