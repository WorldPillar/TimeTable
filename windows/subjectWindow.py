# Form implementation generated from reading ui file 'designUI/subject.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_dialogSubject(object):
    def setupUi(self, dialogSubject):
        dialogSubject.setObjectName("dialogSubject")
        dialogSubject.resize(418, 140)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialogSubject)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.abb_lineEdit = QtWidgets.QLineEdit(parent=dialogSubject)
        self.abb_lineEdit.setObjectName("abb_lineEdit")
        self.gridLayout.addWidget(self.abb_lineEdit, 1, 1, 1, 1)
        self.name_label = QtWidgets.QLabel(parent=dialogSubject)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.abb_label = QtWidgets.QLabel(parent=dialogSubject)
        self.abb_label.setObjectName("abb_label")
        self.gridLayout.addWidget(self.abb_label, 1, 0, 1, 1)
        self.name_lineEdit = QtWidgets.QLineEdit(parent=dialogSubject)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.gridLayout.addWidget(self.name_lineEdit, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=dialogSubject)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dialogSubject)
        self.buttonBox.accepted.connect(dialogSubject.accept) # type: ignore
        self.buttonBox.rejected.connect(dialogSubject.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dialogSubject)

    def retranslateUi(self, dialogSubject):
        _translate = QtCore.QCoreApplication.translate
        dialogSubject.setWindowTitle(_translate("dialogSubject", "Предмет"))
        self.name_label.setText(_translate("dialogSubject", "Название предмета:"))
        self.abb_label.setText(_translate("dialogSubject", "Сокращение:"))
