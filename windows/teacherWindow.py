# Form implementation generated from reading ui file 'designUI/teacher.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_dialogTeacher(object):
    def setupUi(self, dialogTeacher):
        dialogTeacher.setObjectName("dialogTeacher")
        dialogTeacher.resize(353, 209)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialogTeacher)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.family_label = QtWidgets.QLabel(parent=dialogTeacher)
        self.family_label.setObjectName("family_label")
        self.gridLayout.addWidget(self.family_label, 0, 0, 1, 1)
        self.abb_label = QtWidgets.QLabel(parent=dialogTeacher)
        self.abb_label.setObjectName("abb_label")
        self.gridLayout.addWidget(self.abb_label, 2, 0, 1, 1)
        self.name_label = QtWidgets.QLabel(parent=dialogTeacher)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 1, 0, 1, 1)
        self.workload_lineEdit = QtWidgets.QLineEdit(parent=dialogTeacher)
        self.workload_lineEdit.setObjectName("workload_lineEdit")
        self.gridLayout.addWidget(self.workload_lineEdit, 4, 1, 1, 1)
        self.abb_lineEdit = QtWidgets.QLineEdit(parent=dialogTeacher)
        self.abb_lineEdit.setObjectName("abb_lineEdit")
        self.gridLayout.addWidget(self.abb_lineEdit, 2, 1, 1, 1)
        self.workload_label = QtWidgets.QLabel(parent=dialogTeacher)
        self.workload_label.setObjectName("workload_label")
        self.gridLayout.addWidget(self.workload_label, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(parent=dialogTeacher)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(parent=dialogTeacher)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 2, 1, 1)
        self.family_lineEdit = QtWidgets.QLineEdit(parent=dialogTeacher)
        self.family_lineEdit.setObjectName("family_lineEdit")
        self.gridLayout.addWidget(self.family_lineEdit, 0, 1, 1, 2)
        self.name_lineEdit = QtWidgets.QLineEdit(parent=dialogTeacher)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.gridLayout.addWidget(self.name_lineEdit, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=dialogTeacher)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dialogTeacher)
        self.buttonBox.accepted.connect(dialogTeacher.accept) # type: ignore
        self.buttonBox.rejected.connect(dialogTeacher.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dialogTeacher)

    def retranslateUi(self, dialogTeacher):
        _translate = QtCore.QCoreApplication.translate
        dialogTeacher.setWindowTitle(_translate("dialogTeacher", "Учитель"))
        self.family_label.setText(_translate("dialogTeacher", "Фамилия:"))
        self.abb_label.setText(_translate("dialogTeacher", "Сокращение:"))
        self.name_label.setText(_translate("dialogTeacher", "Имя:"))
        self.workload_label.setText(_translate("dialogTeacher", "Нагрузка:"))
        self.label.setText(_translate("dialogTeacher", "(Необязательно)"))
