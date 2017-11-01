import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon
from yapgrep_gui import Ui_MainWindow


class YapgrepGuiProgram(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().__init__()

        self.setupUi(MainWindow)

        self.statusbar.showMessage('__init__')

        self.plainTextEdit.appendPlainText('The quick brown fox jumped over the lazy dogs back')

        self.actionQuit.triggered.connect(self.exitCall)
        self.actionGo.triggered.connect(self.search)

    def search(self):
        self.statusbar.showMessage('Searching . . .')

    def exitCall(self):
        self.statusbar.showMessage('Exit app')
        qApp.quit()


if __name__ == '__main__':
    print('In main')
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = YapgrepGuiProgram(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
