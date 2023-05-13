from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTableWidgetItem

from dialogs.inputdialogs import TeacherDialog, WorkTimeDialog
from schooldata.school import School, Teacher
from windows import tab


class TeacherTab(QtWidgets.QTabWidget, tab.Ui_Form):
    def __init__(self, school: School, headers: [str]):
        super(TeacherTab, self).__init__()
        self.setupUi(self)
        self.headers = headers
        self.school = school

        self.btn_worktime = self.add_button()
        self.set_table()

        self.tableWidget.selectionModel().selectionChanged.connect(self.change_btn_state)
        self.btn_new.clicked.connect(self.new)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_worktime.clicked.connect(self.worktime)

    def add_button(self) -> QtWidgets.QToolButton:
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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        return btn_worktime

    def change_btn_state(self):
        if self.tableWidget.selectedItems():
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)
            self.btn_worktime.setEnabled(True)
        else:
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self.btn_worktime.setEnabled(False)
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
        self.tableWidget.setRowCount(len(self.school.teachers))

        for row in range(self.tableWidget.rowCount()):
            self.update_row(self.tableWidget, self.school.teachers[row], row)
        return

    def new(self):
        dlg = TeacherDialog(self)
        if dlg.exec():
            family = dlg.family_lineEdit.text()
            name = dlg.name_lineEdit.text()
            abb = dlg.abb_lineEdit.text()
            try:
                workload = int(dlg.workload_lineEdit.text())
            except ValueError:
                workload = None
            teacher = Teacher(family, name, workload, abb)
            self.school.teachers.append(teacher)
            self.insert_row(self.tableWidget, teacher)

        self.tableWidget.clearSelection()
        return

    def edit(self):
        position = self.tableWidget.selectedItems()[0].row()
        teacher = self.school.teachers[position]
        dlg = TeacherDialog(self, teacher)
        if dlg.exec():
            family = dlg.family_lineEdit.text()
            name = dlg.name_lineEdit.text()
            abb = dlg.abb_lineEdit.text()
            try:
                workload = int(dlg.workload_lineEdit.text())
            except ValueError:
                workload = None
            teacher.update_data(family, name, workload, abb)
            self.update_row(self.tableWidget, teacher, position)
        return

    def delete(self):
        position = self.tableWidget.selectedItems()[0].row()
        self.tableWidget.removeRow(position)
        self.school.pop_teacher(position)

        self.tableWidget.clearSelection()
        return

    def worktime(self):
        position = self.tableWidget.selectedItems()[0].row()
        teacher = self.school.teachers[position]
        dlg = WorkTimeDialog(self, teacher)
        dlg.exec()
        return
