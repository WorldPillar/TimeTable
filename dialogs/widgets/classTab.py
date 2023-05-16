from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTableWidgetItem

from dialogs.inputdialogs import ClassDialog, WorkTimeDialog
from schooldata.school import School, StudentClass
from windows import tab


class ClassTab(QtWidgets.QTabWidget, tab.Ui_Form):
    """
    Класс вкладки "Классы" списков школы
    """

    def __init__(self, school: School, headers: [str]):
        super(ClassTab, self).__init__()
        self.setupUi(self)
        self.headers = headers
        self.school = school

        self.btn_worktime = self.add_button()
        self.set_table()

        self.tableWidget.selectionModel().selectionChanged.connect(self.change_btn_state)
        self.btn_new.clicked.connect(self._new)
        self.btn_edit.clicked.connect(self._edit)
        self.btn_delete.clicked.connect(self._delete)
        self.btn_worktime.clicked.connect(self.worktime)

    def add_button(self) -> QtWidgets.QToolButton:
        """
        Метод добавляет кнопку Рабочее время.
        """
        line = QtWidgets.QFrame(parent=self)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line.setObjectName("line")
        self.verticalLayout.addWidget(line)
        btn_worktime = QtWidgets.QToolButton(parent=self)
        btn_worktime.setEnabled(False)
        btn_worktime.setObjectName("btn_worktime")
        btn_worktime.setText('Рабочее время')
        btn_worktime.setIcon(QIcon('icons/timeicon.svg'))
        btn_worktime.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.verticalLayout.addWidget(btn_worktime)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        return btn_worktime

    def change_btn_state(self) -> None:
        """
        Метод изменяет состояние кнопок.
        """
        if self.tableWidget.selectedItems():
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)
            self.btn_worktime.setEnabled(True)
        else:
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self.btn_worktime.setEnabled(False)
        return

    def insert_row(self, table, new_obj) -> None:
        """
        Добавляет новую строчку в таблицу.
        :param table: Таблица, в которую добавляется строчка.
        :param new_obj: Объект, который помещается в таблицу.
        """
        rowcount = table.rowCount()
        table.insertRow(rowcount)
        self._update_row(table, new_obj, rowcount)
        return

    @staticmethod
    def _update_row(table, new_obj, row) -> None:
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
        return

    def set_table(self) -> None:
        """
        Создание таблицы.
        """
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setRowCount(len(self.school.student_classes))

        for row in range(self.tableWidget.rowCount()):
            self._update_row(self.tableWidget, self.school.student_classes[row], row)
        return

    def _new(self) -> None:
        """
        Метод создания нового объекта.
        """
        dlg = ClassDialog(self)
        if dlg.exec():
            name = dlg.name_lineEdit.text()
            abb = dlg.abb_lineEdit.text()
            student_class = StudentClass(name, abb)
            self.school.student_classes.append(student_class)
            self.insert_row(self.tableWidget, student_class)

        self.tableWidget.clearSelection()
        return

    def _edit(self) -> None:
        """
        Метод редактирования информации выбранного объекта таблицы.
        """
        position = self.tableWidget.selectedItems()[0].row()
        student_class = self.school.student_classes[position]
        dlg = ClassDialog(self, student_class)
        if dlg.exec():
            name = dlg.name_lineEdit.text()
            abb = dlg.abb_lineEdit.text()
            student_class.update_data(name, abb)
            self._update_row(self.tableWidget, student_class, position)
        return

    def _delete(self) -> None:
        """
        Метод удаления выбранного объекта таблицы.
        """
        position = self.tableWidget.selectedItems()[0].row()
        self.tableWidget.removeRow(position)
        self.school.pop_class(position)

        self.tableWidget.clearSelection()
        return

    def worktime(self) -> None:
        """
        Метод вызова диалогового окна редактирования рабочей недели выбранного объекта.
        """
        position = self.tableWidget.selectedItems()[0].row()
        student_class = self.school.student_classes[position]
        dlg = WorkTimeDialog(self, student_class)
        dlg.exec()
        return
