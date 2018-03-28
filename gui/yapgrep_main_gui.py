import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QAction, qApp, QApplication, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from yapgrep_gui import Ui_MainWindow
from yapgrep_common_gui import Ui_Common
import os
from os.path import join, getsize
import glob
import regex
from timeit import default_timer as timer
from icecream import ic
from datetime import datetime
import argparse

def unixTimestamp():
    return '%s |> ' % datetime.now()

ic.configureOutput(prefix=unixTimestamp)


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
        ic('Directory from user: {}'.format(directory))
        try:
            self.walkDirs(directory, reg)
        except:
            ic("Some error occurred!".join(sys.exc_info()))
        self.end = timer()
        self.textEdit.append('Time: {:.2f}'.format(self.end - self.start))
        self.statusbar.showMessage('Searching completed.')

    def walkDirs(self, fileSpec, pattern):
        fs = os.path.expanduser(fileSpec)
        ic(fs)

        fs = os.path.expandvars(fs)
        ic(fs)

        base = os.path.basename(fs)
        ic(base)

        path = os.path.dirname(fs)
        ic(path)

        if os.path.isdir(fs):
            fs += '/**'
        elif os.path.isdir(path):
            fs = path + '/**/' + base

        ic(fs)
        ic(self.recursive)

        for p in glob.iglob(fs, recursive=self.recursive):
            if os.path.isfile(p):
                buf = self.grepFile(p, pattern)
                if buf:
                    self.textEdit.append('file: {}'.format(p))
                    self.textEdit.append("".join(buf))

        ic(fs)
        self.textEdit.append('Files searched: {}, Matches found: {}'.format(self.files, self.matches))
        ic('Files searched: {}, Matches found: {}'.format(self.files, self.matches))


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

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-r", "-R", "--recurse", help="recurse down the directory tree", action="store_true", default=True)
    argparser.add_argument("-n", "--no-recurse", help="don't recurse down the directory tree", action="store_false", dest="recurse")
    argparser.add_argument("pattern")
    argparser.add_argument("filedirs", nargs="+", type=list)  # How do we make this OPTIONAL??????
    args = argparser.parse_args()

    print(args.filedirs)

    MainWindow = QtWidgets.QMainWindow()

    ui = YapgrepGuiProgram(MainWindow)

    ic(args)
    ic(args.recurse)
    ui.recursive = args.recurse

    ui.ui2.checkBox.setChecked(ui.recursive)
    ui.lineEdit.setText(QtCore.QCoreApplication.translate("MainWindow", ' '.join([''.join(args.filedirs[i]) for i in range(len(args.filedirs))])))
    ui.lineEdit_2.setText(QtCore.QCoreApplication.translate("MainWindow", args.pattern))

    MainWindow.show()

    sys.exit(app.exec_())
