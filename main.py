from Interface import main_window

from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = main_window.MainWindow()

    window.showMaximized()

    sys.exit(app.exec_())