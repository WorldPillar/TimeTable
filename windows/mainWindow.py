# Form implementation generated from reading ui file 'designUI/design.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

from dialogs.widgets.tablewidget import MyTableWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1226, 810)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 6, 0, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tbtn_newfile = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_newfile.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("designUI\\../icons/newfileicon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_newfile.setIcon(icon)
        self.tbtn_newfile.setIconSize(QtCore.QSize(32, 32))
        self.tbtn_newfile.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_newfile.setAutoRaise(True)
        self.tbtn_newfile.setObjectName("tbtn_newfile")
        self.horizontalLayout.addWidget(self.tbtn_newfile)
        self.tbtn_open = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_open.setEnabled(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("designUI\\../icons/openfileicon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_open.setIcon(icon1)
        self.tbtn_open.setIconSize(QtCore.QSize(32, 32))
        self.tbtn_open.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_open.setAutoRaise(True)
        self.tbtn_open.setObjectName("tbtn_open")
        self.horizontalLayout.addWidget(self.tbtn_open)
        self.tbtn_save = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_save.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbtn_save.sizePolicy().hasHeightForWidth())
        self.tbtn_save.setSizePolicy(sizePolicy)
        self.tbtn_save.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("designUI\\../icons/savefileicon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_save.setIcon(icon2)
        self.tbtn_save.setIconSize(QtCore.QSize(32, 32))
        self.tbtn_save.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.tbtn_save.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_save.setAutoRaise(True)
        self.tbtn_save.setObjectName("tbtn_save")
        self.horizontalLayout.addWidget(self.tbtn_save)
        self.tbtn_export = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_export.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("designUI\\../icons/exporticon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_export.setIcon(icon3)
        self.tbtn_export.setIconSize(QtCore.QSize(48, 32))
        self.tbtn_export.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.tbtn_export.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_export.setAutoRaise(True)
        self.tbtn_export.setObjectName("tbtn_export")
        self.horizontalLayout.addWidget(self.tbtn_export)
        self.line = QtWidgets.QFrame(parent=self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.tbtn_subject = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_subject.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("designUI\\../icons/subjecticon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_subject.setIcon(icon4)
        self.tbtn_subject.setIconSize(QtCore.QSize(32, 32))
        self.tbtn_subject.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_subject.setAutoRaise(True)
        self.tbtn_subject.setObjectName("tbtn_subject")
        self.horizontalLayout.addWidget(self.tbtn_subject)
        self.tbtn_class = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_class.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("designUI\\../icons/classicon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_class.setIcon(icon5)
        self.tbtn_class.setIconSize(QtCore.QSize(48, 32))
        self.tbtn_class.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_class.setAutoRaise(True)
        self.tbtn_class.setObjectName("tbtn_class")
        self.horizontalLayout.addWidget(self.tbtn_class)
        self.tbtn_teacher = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_teacher.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("designUI\\../icons/teachericon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_teacher.setIcon(icon6)
        self.tbtn_teacher.setIconSize(QtCore.QSize(30, 32))
        self.tbtn_teacher.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_teacher.setAutoRaise(True)
        self.tbtn_teacher.setObjectName("tbtn_teacher")
        self.horizontalLayout.addWidget(self.tbtn_teacher)
        self.tbtn_lesson = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_lesson.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("designUI\\../icons/lessonicon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_lesson.setIcon(icon7)
        self.tbtn_lesson.setIconSize(QtCore.QSize(46, 32))
        self.tbtn_lesson.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_lesson.setAutoRaise(True)
        self.tbtn_lesson.setObjectName("tbtn_lesson")
        self.horizontalLayout.addWidget(self.tbtn_lesson)
        self.line_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.tbtn_scheduling = QtWidgets.QToolButton(parent=self.centralwidget)
        self.tbtn_scheduling.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("designUI\\../icons/scheduleicon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tbtn_scheduling.setIcon(icon8)
        self.tbtn_scheduling.setIconSize(QtCore.QSize(48, 32))
        self.tbtn_scheduling.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tbtn_scheduling.setAutoRaise(True)
        self.tbtn_scheduling.setObjectName("tbtn_scheduling")
        self.horizontalLayout.addWidget(self.tbtn_scheduling)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget_days = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget_days.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_days.sizePolicy().hasHeightForWidth())
        self.tableWidget_days.setSizePolicy(sizePolicy)
        self.tableWidget_days.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.tableWidget_days.setFont(font)
        self.tableWidget_days.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.tableWidget_days.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.tableWidget_days.setAutoScroll(True)
        self.tableWidget_days.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_days.setProperty("showDropIndicator", False)
        self.tableWidget_days.setDragDropOverwriteMode(False)
        self.tableWidget_days.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.tableWidget_days.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.tableWidget_days.setObjectName("tableWidget_days")
        self.tableWidget_days.setColumnCount(0)
        self.tableWidget_days.setRowCount(0)
        self.tableWidget_days.horizontalHeader().setVisible(False)
        self.tableWidget_days.horizontalHeader().setDefaultSectionSize(0)
        self.tableWidget_days.horizontalHeader().setHighlightSections(False)
        self.tableWidget_days.horizontalHeader().setMinimumSectionSize(0)
        self.tableWidget_days.verticalHeader().setVisible(True)
        self.tableWidget_days.verticalHeader().setDefaultSectionSize(0)
        self.tableWidget_days.verticalHeader().setHighlightSections(False)
        self.tableWidget_days.verticalHeader().setMinimumSectionSize(0)
        self.verticalLayout_2.addWidget(self.tableWidget_days)
        self.tableWidget_timetable = MyTableWidget(parent=self.centralwidget, mainapp=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_timetable.sizePolicy().hasHeightForWidth())
        self.tableWidget_timetable.setSizePolicy(sizePolicy)
        self.tableWidget_timetable.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.tableWidget_timetable.setAutoScroll(True)
        self.tableWidget_timetable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_timetable.setDragEnabled(True)
        self.tableWidget_timetable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget_timetable.setObjectName("tableWidget_timetable")
        self.tableWidget_timetable.setColumnCount(0)
        self.tableWidget_timetable.setRowCount(0)
        self.tableWidget_timetable.horizontalHeader().setDefaultSectionSize(0)
        self.tableWidget_timetable.horizontalHeader().setMinimumSectionSize(0)
        self.tableWidget_timetable.verticalHeader().setDefaultSectionSize(0)
        self.tableWidget_timetable.verticalHeader().setMinimumSectionSize(0)
        self.verticalLayout_2.addWidget(self.tableWidget_timetable)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Расписание"))
        self.tbtn_newfile.setText(_translate("MainWindow", "Новый файл"))
        self.tbtn_open.setText(_translate("MainWindow", "Открыть"))
        self.tbtn_save.setText(_translate("MainWindow", "Сохранить"))
        self.tbtn_export.setText(_translate("MainWindow", "Экспорт расписания"))
        self.tbtn_subject.setText(_translate("MainWindow", "Предметы"))
        self.tbtn_class.setText(_translate("MainWindow", "Классы"))
        self.tbtn_teacher.setText(_translate("MainWindow", "Учителя"))
        self.tbtn_lesson.setText(_translate("MainWindow", "Уроки"))
        self.tbtn_scheduling.setText(_translate("MainWindow", "Составить расписание"))
