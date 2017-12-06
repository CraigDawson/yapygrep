import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon
from yapgrep_gui import Ui_MainWindow
import os
from os.path import join, getsize


class YapgrepGuiProgram(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().__init__()

        self.setupUi(MainWindow)

        self.statusbar.showMessage('__init__')

        self.plainTextEdit.appendPlainText('The quick brown fox jumped over the lazy dogs back')

        self.actionQuit.triggered.connect(self.exitCall)
        self.actionGo.triggered.connect(self.search)
        self.pushButton.clicked.connect(self.search)

    def search(self):
        self.statusbar.showMessage('Searching . . .')
        print('Searching...')
        self.dirWalk("..")
        
    def dirWalk(self, directory):
        print('dir: ' + directory)
        try:
            for root, dirs, files in os.walk(directory):
                print(root)
                print('Dirs: ')
                print(dirs)
                print('Files: {}'.format(files))
                print(root, "consumes", end=" ")
                print(sum(getsize(join(root, name)) for name in files), end=" ")
                print("bytes in", len(files), "non-directory files")
                if '.git' in dirs:
                    dirs.remove('.git')  # don't visit CVS directories
        except:
            print ("any error!")
            
    def exitCall(self):
        self.statusbar.showMessage('Exit app')
        qApp.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = YapgrepGuiProgram(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
