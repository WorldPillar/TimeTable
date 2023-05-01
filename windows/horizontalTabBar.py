from PyQt6.QtCore import Qt, QRectF, QSize
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QTabBar, QStylePainter, QStyleOptionTab, QStyle


class TabBar(QTabBar):
    SIZE = QSize(70, 66)
    ICONS_SIZES = [QSize(32, 32), QSize(48, 32),
                   QSize(30, 32), QSize(46, 32)]

    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QStyle.ControlElement.CE_TabBarTabShape, option)

            painter.drawText(self.tabRect(index),
                             Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextDontClip,
                             self.tabText(index))

            left = (self.SIZE.width() - self.ICONS_SIZES[index].width()) / 2
            top = self.SIZE.height() * (index + 1) - self.ICONS_SIZES[index].height() - 10
            width = self.ICONS_SIZES[index].width()
            height = self.ICONS_SIZES[index].height()
            match index:
                case 0:
                    painter.drawImage(QRectF(left, top, width, height), QImage("icons/subjecticon.svg"))
                case 1:
                    painter.drawImage(QRectF(left, top, width, height), QImage("icons/classicon.svg"))
                case 2:
                    painter.drawImage(QRectF(left, top, width, height), QImage("icons/teachericon.svg"))
                case 3:
                    painter.drawImage(QRectF(left, top, width, height), QImage("icons/lessonicon.svg"))

    def tabSizeHint(self, index):
        # size = QTabBar.tabSizeHint(self, index)
        size = self.SIZE
        if size.width() < size.height():
            size.transpose()
        return size
