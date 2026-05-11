import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QIcon

from main_window import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    if QFile.exists('pictures/icon.ico'):
        window.setWindowIcon(QIcon('pictures/icon.ico'))
    sys.exit(app.exec_())