import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, qApp, QApplication, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from yapgrep_gui import Ui_MainWindow
from yapgrep_common_gui import Ui_Common
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

        self.Common = QDialog()
        self.ui2 = Ui_Common()
        self.ui2.setupUi(self.Common)

        self.recursive = True
        self.ui2.checkBox.setChecked(self.recursive)

        self.statusbar.showMessage('ready')

        f = self.textEdit.font()
        f.setFamily("Courier New")
        f.setPointSize(18)
        self.textEdit.setFont(f)

        self.textEdit.append('yapgrep {}'.format(self.version))

        self.actionQuit.triggered.connect(self.exitCall)
        self.actionGo.triggered.connect(self.search)
        self.pushButton.clicked.connect(self.search)
        self.actionCommon.triggered.connect(self.common_settings)
        self.actionAbout.triggered.connect(self.about)

    def common_settings(self):
        self.Common.exec_()
        self.recursive = self.ui2.checkBox.isChecked()

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
        self.textEdit.clear()
        directory = self.lineEdit.text()
        pattern = self.lineEdit_2.text()
        pattern = '(' + pattern + ')'
        reg = regex.compile(pattern)
        self.start = timer()
        print('Directory from user:', directory)
        try:
            self.walkDirs(directory, reg)
        except:
            print ("some error occurred!", sys.exc_info())
        self.end = timer()
        self.textEdit.append('Time: {:.2f}'.format(self.end - self.start))
        self.statusbar.showMessage('Searching completed.')

    def dbg(self, prefix, item):
        print(prefix + ':', item)

    def walkDirs(self, fileSpec, pattern):
        fs = os.path.expanduser(fileSpec)
        self.dbg('fs/expanduser', fs)

        fs = os.path.expandvars(fs)
        self.dbg('fs/expandvars', fs)

        base = os.path.basename(fs)
        self.dbg('base', base)

        path = os.path.dirname(fs)
        self.dbg('path', path)

        if os.path.isdir(fs):
            fs += '/**'
        elif os.path.isdir(path):
            fs = path + '/**/' + base

        self.dbg('fs', fs)
        self.dbg('recursive', self.recursive)

        for p in glob.iglob(fs, recursive=self.recursive):
            if os.path.isfile(p):
                buf = self.grepFile(p, pattern)
                if buf:
                    self.textEdit.append('file: {}'.format(p))
                    self.textEdit.append("".join(buf))

        self.dbg('Final fs', fs)
        self.textEdit.append('Files searched: {}, Matches found: {}'.format(self.files, self.matches))
        print('Files searched: {}, Matches found: {}'.format(self.files, self.matches))


    def grepFile(self, fileName, pattern):
        global app
        self.statusbar.showMessage(fileName)
        app.processEvents()
        buf = []
        with open(fileName, 'r') as f:
            try:
                self.files += 1
                for i, line in enumerate(f):
                    if pattern.search(line):
                        self.matches += 1
                        newLine = regex.sub(pattern, r'<font color="red"><b>\1</b></font>', line)
                        buf.append('&nbsp;&nbsp;&nbsp;&nbsp;{}:{}<br>'.format('<font color="blue">'+str(i)+'</font>', newLine))
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
