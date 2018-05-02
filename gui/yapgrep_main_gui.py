import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import qApp, QMessageBox, QDialog
from yapgrep_gui import Ui_MainWindow
from yapgrep_common_gui import Ui_Common
import os
import glob
import regex
from timeit import default_timer as timer
from icecream import ic
from datetime import datetime
import argparse
import html
import json


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

        self.typeList = []

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

        for d in directory.split(':'):
            self.start = timer()
            ic('Directory from user: {}'.format(d))

            try:
                self.walkDirs(d, reg)
            except:
                ic("Some error occurred!".join(sys.exc_info()))
            self.end = timer()
            self.textEdit.append('Time: {:.2f}'.format(self.end - self.start))

        self.statusbar.showMessage('Searching completed.')

    def checkExtInTypeList(self, ext):
        if self.typeList == []:
            return True

        if ext[1:] in self.typeList:
            return True

        return False


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
            (root, ext) = os.path.splitext(p)
            if os.path.isfile(p) and self.checkExtInTypeList(ext):
                buf = self.grepFile(p, pattern)
                if buf:
                    self.textEdit.append('file: {}'.format(p))
                    self.textEdit.append("".join(buf))

        ic(fs)
        self.textEdit.append('Files searched: {}, Matches found: {}'.format(self.files, self.matches))
        ic('Files searched: {}, Matches found: {}'.format(self.files, self.matches))
        self.files,self.matches = 0,0

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
                        # escape HTML in line
                        line = html.escape(line)
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
    argparser.add_argument("-g", "--go", help="implicitly push the search button", action="store_true")
    argparser.add_argument("-t", "--type", help="specify filetypes for search", action="append", dest="ftype")

    argparser.add_argument("pattern", nargs="?", default="")
    argparser.add_argument("filedirs", nargs="*", default=[os.getcwd()])
    args = argparser.parse_args()

    ic(args.filedirs)

    MainWindow = QtWidgets.QMainWindow()

    ui = YapgrepGuiProgram(MainWindow)

    ic(args)
    ic(args.recurse)
    ui.recursive = args.recurse

    ui.ui2.checkBox.setChecked(ui.recursive)
    ui.lineEdit.setText(QtCore.QCoreApplication.translate("MainWindow", ':'.join(args.filedirs)))
    ui.lineEdit_2.setText(QtCore.QCoreApplication.translate("MainWindow", args.pattern))

    MainWindow.show()

    # Read in valid types
    with open('types.json', 'r') as f:
        types = json.load(f)
        # TODO add types to GUI

    # Find user selected type
    if args.ftype is not None:
        for t in args.ftype:
            if t in types:
                ui.typeList += types[t]
                ic(ui.typeList)
            else:
                msg = 'User specified type not found: {}'.format(t)
                ic(msg)
                ui.textEdit.append('<font color="red">{}</font>'.format(msg))

    if args.go:
        if len(args.pattern) > 0:
            ui.search()
        else:
            ui.textEdit.append('<font color="red">No pattern specified</font>')

    sys.exit(app.exec_())
