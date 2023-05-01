# Form implementation generated from reading ui file 'designUI/school.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_dialogSchool(object):
    def setupUi(self, dialogSchool):
        dialogSchool.setObjectName("dialogSchool")
        dialogSchool.resize(536, 207)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialogSchool)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.name_label = QtWidgets.QLabel(parent=dialogSchool)
        self.name_label.setObjectName("name_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.name_label)
        self.name_lineEdit = QtWidgets.QLineEdit(parent=dialogSchool)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.name_lineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtWidgets.QFrame(parent=dialogSchool)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setObjectName("formLayout_2")
        self.amount_lessons_label = QtWidgets.QLabel(parent=dialogSchool)
        self.amount_lessons_label.setObjectName("amount_lessons_label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.amount_lessons_label)
        self.amount_days_label = QtWidgets.QLabel(parent=dialogSchool)
        self.amount_days_label.setObjectName("amount_days_label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.amount_days_label)
        self.amount_lessons_combobox = QtWidgets.QComboBox(parent=dialogSchool)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount_lessons_combobox.sizePolicy().hasHeightForWidth())
        self.amount_lessons_combobox.setSizePolicy(sizePolicy)
        self.amount_lessons_combobox.setMinimumSize(QtCore.QSize(30, 0))
        self.amount_lessons_combobox.setBaseSize(QtCore.QSize(30, 0))
        self.amount_lessons_combobox.setObjectName("amount_lessons_combobox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.amount_lessons_combobox)
        self.amount_days_combobox = QtWidgets.QComboBox(parent=dialogSchool)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount_days_combobox.sizePolicy().hasHeightForWidth())
        self.amount_days_combobox.setSizePolicy(sizePolicy)
        self.amount_days_combobox.setMinimumSize(QtCore.QSize(30, 0))
        self.amount_days_combobox.setBaseSize(QtCore.QSize(30, 0))
        self.amount_days_combobox.setObjectName("amount_days_combobox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.amount_days_combobox)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=dialogSchool)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dialogSchool)
        self.buttonBox.accepted.connect(dialogSchool.accept) # type: ignore
        self.buttonBox.rejected.connect(dialogSchool.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dialogSchool)

    def retranslateUi(self, dialogSchool):
        _translate = QtCore.QCoreApplication.translate
        dialogSchool.setWindowTitle(_translate("dialogSchool", "Настройки школы"))
        self.name_label.setText(_translate("dialogSchool", "Название учреждения:"))
        self.amount_lessons_label.setText(_translate("dialogSchool", "Число уроков в день:"))
        self.amount_days_label.setText(_translate("dialogSchool", "Число учебных дней:"))
