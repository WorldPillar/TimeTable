from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox


def showMessage(title: str, message: str):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
    msg.setWindowFlag(Qt.WindowType.WindowTitleHint, True)
    msg.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)
    msg.exec()
