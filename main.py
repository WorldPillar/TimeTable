import sys

from PyQt6.QtWidgets import QApplication, QStyleFactory

from dialogs.mainapp import MainApp


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
