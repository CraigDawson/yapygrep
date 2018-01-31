import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, qApp, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from yapgrep_gui import Ui_MainWindow
import os
from os.path import join, getsize
import glob
import regex
from timeit import default_timer as timer


class YapgrepGuiProgram(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().__init__()

        self.version = 0.5

        self.setupUi(MainWindow)

        self.statusbar.showMessage('ready')

        f = self.plainTextEdit.font()
        f.setFamily("Courier New")
        f.setPointSize(18)
        self.plainTextEdit.setFont(f)

        self.plainTextEdit.appendPlainText('yapgrep {}'.format(self.version))

        self.actionQuit.triggered.connect(self.exitCall)
        self.actionGo.triggered.connect(self.search)
        self.pushButton.clicked.connect(self.search)
        
        self.actionAbout.triggered.connect(self.about)

    def about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Yapygrep " + str(self.version))
#        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("About")
#        msg.setDetailedText("The details are as follows:")

        msg.exec_()
        
    def search(self):
        self.files = 0
        self.matches = 0
        self.statusbar.showMessage('Searching . . .')
        self.plainTextEdit.clear()
        directory = self.lineEdit.text()
        pattern = self.lineEdit_2.text()
        reg = regex.compile(pattern)
        self.start = timer()
        print('Directory from user:', directory)
        try:
            self.walkDirs(directory, reg)
        except:
            print ("some error occurred!", sys.exc_info())
        self.end = timer()
        self.plainTextEdit.appendPlainText('Time: {:.2f}'.format(self.end - self.start))
        self.statusbar.showMessage('Searching completed.')

    def dbg(self, prefix, item):
        print(prefix + ':', item)

    def walkDirs(self, fileSpec, pattern):
        fs = os.path.expanduser(fileSpec)
        self.dbg('fs/expanduser', fs)

        fs = os.path.expandvars(fs)
        self.dbg('fs/expandvars', fs)

        if os.path.isdir(fs):
            self.dbg('fs', 'adding "/**" to dir')
            fs += '/**'

        base = os.path.basename(fs)
        self.dbg('base', base)

        path = os.path.dirname(fs)
        self.dbg('path', path)

        for p in glob.iglob(fs, recursive=True):
            if os.path.isfile(p):
                buf = self.grepFile(p, pattern)
                if buf:
                    self.plainTextEdit.appendPlainText('file: {}'.format(p))
                    self.plainTextEdit.appendPlainText("".join(buf))

        self.dbg('Final fs', fs)
        self.plainTextEdit.appendPlainText('Files searched: {}, Matches found: {}'.format(self.files, self.matches))
        print('Files searched: {}, Matches found: {}'.format(self.files, self.matches))


    def grepFile(self, fileName, pattern):
        global app
        buf = []
        with open(fileName, 'r') as f:
            try:
                self.files += 1
                self.statusbar.showMessage(fileName)
                app.processEvents()
                for i, line in enumerate(f):
                    if pattern.search(line):
                        self.matches += 1
                        buf.append('    {}:{}'.format(i, line))
            except UnicodeDecodeError:
                pass
        return buf



    def exitCall(self):
        self.statusbar.showMessage('Exit app')
        qApp.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = YapgrepGuiProgram(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
