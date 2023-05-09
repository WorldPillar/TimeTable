import ctypes
import sys

from PyQt6.QtWidgets import QApplication, QStyleFactory

from dialogs.mainapp import MainApp


myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
