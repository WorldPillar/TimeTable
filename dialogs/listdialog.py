from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QDialogButtonBox
from PyQt6.QtCore import Qt

from dialogs.widgets import subjectTab, classTab, teacherTab, lessonTab
from schooldata.data import SchoolData
from schooldata.school import School
from windows import listsWindow


class ListDialog(QDialog, listsWindow.Ui_dialogLists):
    """
    Диалоговое окно списков школы.
    """

    def __init__(self, parent, school: School):
        super(ListDialog, self).__init__(parent)
        self.setupUi(self)
        self.school = school

        self.buttonBox.button(QDialogButtonBox.StandardButton.Close).setText('Закрыть')
        self.setWindowIcon(QIcon())
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        self.subject_tab = subjectTab.SubjectTab(self.school, SchoolData.headers["Subject"])
        self.class_tab = classTab.ClassTab(self.school, SchoolData.headers["Class"])
        self.teacher_tab = teacherTab.TeacherTab(self.school, SchoolData.headers["Teacher"])
        self.lesson_tab = lessonTab.LessonTab(self.school, SchoolData.headers["Lesson"])

        self.tabWidget.addTab(self.subject_tab, 'Предметы')
        self.tabWidget.addTab(self.class_tab, 'Классы')
        self.tabWidget.addTab(self.teacher_tab, 'Учителя')
        self.tabWidget.addTab(self.lesson_tab, 'Уроки')

        self.tabWidget.currentChanged.connect(self.update_table)

    def update_table(self) -> None:
        """
        Метод вызывается после смены вкладки диалогового окна. В зависимости от активной вкладки, обновляет её таблицу.
        """
        index = self.tabWidget.currentIndex()
        match index:
            case 0:
                self.subject_tab.set_table()
            case 1:
                self.class_tab.set_table()
            case 2:
                self.teacher_tab.set_table()
            case 3:
                self.lesson_tab.set_table()
        return
