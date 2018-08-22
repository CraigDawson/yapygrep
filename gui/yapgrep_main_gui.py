import argparse
import glob
import html
import json
import os
import sys
from datetime import datetime

import regex
from icecream import ic
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QMessageBox, qApp

from yapgrep_common_gui import Ui_Common
from yapgrep_gui import Ui_MainWindow

types = {}  # type dict from json file


def unixTimestamp():
    return "%s |> " % datetime.now()


ic.configureOutput(prefix=unixTimestamp)


class YapCancel(Exception):
    pass


class CommonDialog(Ui_Common):
    def __init__(self, Common):
        super().__init__()
        self.setupUi(Common)
        self.checkBox_3.stateChanged.connect(self.lineChange)

    def lineChange(self, i):
        if not self.checkBox_3.isChecked():
            self.checkBox_4.setChecked(False)

        self.checkBox_4.setEnabled(self.checkBox_3.isChecked())


class YapgrepGuiProgram(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().__init__()

        self.version = 0.6

        self.setupUi(MainWindow)

        self.Common = QDialog()
        self.ui2 = CommonDialog(self.Common)

        self.buf = []

        self.recursive = True
        self.ignorecase = False
        self.linenumber = True
        self.column = False
        self.smartcase = True
        self.raw = False
        self.ruler = False

        self.searching = False

        self.ui2.checkBox.setChecked(self.recursive)
        self.ui2.checkBox_2.setChecked(self.ignorecase)
        self.ui2.checkBox_3.setChecked(self.linenumber)
        self.ui2.checkBox_4.setChecked(self.column)
        self.ui2.checkBox_5.setChecked(self.smartcase)
        self.ui2.checkBox_6.setChecked(self.raw)
        self.ui2.checkBox_7.setChecked(self.ruler)

        ic(self.ui2.checkBox_3.isChecked())
        self.ui2.checkBox_4.setEnabled(self.ui2.checkBox_3.isChecked())

        self.statusbar.showMessage("ready")

        self.typeList = []  # list of file exts

        f = self.textEdit.font()
        f.setFamily("Courier New")
        f.setPointSize(18)
        self.textEdit.setFont(f)

        self.textEdit.append("yapgrep {}".format(self.version))

        self.actionQuit.triggered.connect(self.exitCall)
        self.actionGo.triggered.connect(self.search)
        self.pushButton.clicked.connect(self.search)
        self.actionCommon.triggered.connect(self.common_settings)
        self.actionAbout.triggered.connect(self.about)

    def common_settings(self):
        self.Common.exec_()
        self.recursive = self.ui2.checkBox.isChecked()
        self.ignorecase = self.ui2.checkBox_2.isChecked()
        self.linenumber = self.ui2.checkBox_3.isChecked()
        self.column = self.ui2.checkBox_4.isChecked()
        self.smartcase = self.ui2.checkBox_5.isChecked()
        self.raw = self.ui2.checkBox_6.isChecked()
        self.ruler = self.ui2.checkBox_7.isChecked()

    def about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Yapygrep " + str(self.version))
        #        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("About")
        #        msg.setDetailedText("The details are as follows:")

        msg.exec_()

    def cancel(self):
        raise YapCancel("Cancel", "Canceled")

    def printRuler(self, fmt, line, ln=None, cn=None):
        s = ""
        for n in range(8):
            s += str(n) + " " * 9

        #  '<font color="blue">{}:{}:</font>{}'
        if not self.raw:
            self.buf.append('<font color="gray">')

        if ln and cn:
            self.outputLine(fmt.format(str(ln), str(cn), s))
            self.outputLine(fmt.format(str(ln), str(cn), "|123456789" * 8))
        elif ln:
            self.outputLine(fmt.format(str(ln), s))
            self.outputLine(fmt.format(str(ln), "|123456789" * 8))
        else:
            self.outputLine(s)
            self.outputLine("|123456789" * 8)

        if not self.raw:
            self.buf.append('</font>')

    def search(self):
        if self.searching:
            self.searching = False
            return

        self.searching = True
        self.pushButton.setText("&Cancel")
        try:
            self.files = 0
            self.matchedFiles = 0
            self.matches = 0
            self.statusbar.showMessage("Searching . . .")
            self.textEdit.clear()
            directory = self.lineEdit.text()
            pattern = self.lineEdit_2.text()
            pattern = "(" + pattern + ")"
            if self.ignorecase or (pattern.islower() and self.smartcase):
                reg = regex.compile(pattern, flags=regex.IGNORECASE)
            else:
                reg = regex.compile(pattern)

            for d in directory.split(":"):
                self.start = datetime.now()
                ic("Directory from user: {}".format(d))

                try:
                    self.walkDirs(d, reg)
                except YapCancel:
                    pass
                except:  # noqa: E722
                    ic("Some error occurred!".join(sys.exc_info()))

            self.end = datetime.now()
            self.textEdit.append("Time: {}".format(self.end - self.start))
        except YapCancel:
            print("Cancel button pushed, caught in search()")
            self.statusbar.showMessage("Searching Canceled.")
        finally:
            self.pushButton.setText("&Search")
            self.searching = False

        self.statusbar.showMessage("Searching completed.")

    def checkExtInTypeList(self, ext):
        if self.typeList == []:
            return True

        if ext[1:] in self.typeList:
            return True

        return False

    def walkDirs(self, fileSpec, pattern):
        fs = os.path.expanduser(fileSpec)

        fs = os.path.expandvars(fs)

        base = os.path.basename(fs)

        path = os.path.dirname(fs)

        if os.path.isdir(fs):
            fs += "/**"
        elif os.path.isdir(path):
            fs = path + "/**/" + base

        global types
        self.typeList = []
        for i in range(ui.ui2.listWidget.count()):
            if ui.ui2.listWidget.item(i).checkState() == QtCore.Qt.Checked:
                self.typeList += types[str(ui.ui2.listWidget.item(i).text())]
                ic(types[str(ui.ui2.listWidget.item(i).text())])

        ic(fs)

        for p in glob.iglob(fs, recursive=self.recursive):
            (root, ext) = os.path.splitext(p)
            if os.path.isfile(p) and self.checkExtInTypeList(ext):
                """ Grep the file """
                self.buf = self.grepFile(p, pattern)
                if self.buf:
                    self.textEdit.append("file: {}".format(p))
                    self.textEdit.append("".join(self.buf))

        fmt = "Files searched: {}, Matched files: {}, Matches found: {}"
        print(fmt.format(self.files, self.matchedFiles, self.matches))
        self.textEdit.append(
            fmt.format(self.files, self.matchedFiles, self.matches))
        ic(fmt.format(self.files, self.matchedFiles, self.matches))
        self.files, self.matchedFiles, self.matches = 0, 0, 0

    def grepFile(self, fileName, pattern):
        global app
        self.statusbar.showMessage(fileName)
        app.processEvents(
        )  # TODO: move into file loop with (i % 10000) == 0 ???
        if not self.searching:
            raise YapCancel
        self.buf = []
        matchFound = False
        with open(fileName, "r") as f:
            try:
                self.files += 1
                for i, line in enumerate(f):
                    if pattern.search(line):
                        self.matches += 1
                        matchFound = True
                        line = line.rstrip("\n")
                        if self.linenumber:
                            if self.column:
                                for m in regex.finditer(pattern, line):
                                    c = m.start()
                                    break
                                line = html.escape(line)
                                line = (line if self.raw else regex.sub(
                                    pattern,
                                    r'<font color="red"><b>\1</b></font>',
                                    line,
                                ))
                                fmt = ("{}:{}:{}" if self.raw else
                                       '<font color="blue">{}:{}:</font>{}')

                                if self.ruler:
                                    self.printRuler(fmt, line, i, c)

                                self.outputLine(
                                    fmt.format(str(i), str(c), line))
                            else:
                                line = html.escape(line)
                                line = (line if self.raw else regex.sub(
                                    pattern,
                                    r'<font color="red"><b>\1</b></font>',
                                    line,
                                ))
                                fmt = ("{}:{}" if self.raw else
                                       '<font color="blue">{}:</font>{}')
                                if self.ruler:
                                    self.printRuler(fmt, line, i)

                                self.outputLine(fmt.format(str(i), line))
                        else:
                            line = html.escape(line)
                            line = (line if self.raw else regex.sub(
                                pattern, r'<font color="red"><b>\1</b></font>',
                                line))
                            if self.ruler:
                                self.printRuler("{}", line)
                            self.outputLine(line)
            except UnicodeDecodeError:
                pass
        if matchFound:
            self.matchedFiles += 1
        return self.buf

    def exitCall(self):
        self.statusbar.showMessage("Exit app")
        qApp.quit()

    def outputLine(self, line):
        self.buf.append("<pre><code>" + line + "</code></pre>")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-r",
        "-R",
        "--recurse",
        help="recurse down the directory tree",
        action="store_true",
        default=True,
    )
    argparser.add_argument(
        "-n",
        "--no-recurse",
        help="don't recurse down the directory tree",
        action="store_false",
        dest="recurse",
    )
    argparser.add_argument(
        "-g",
        "--go",
        help="implicitly push the search button",
        action="store_true")
    argparser.add_argument(
        "-t",
        "--type",
        help="specify filetypes for search",
        action="append",
        dest="ftype",
    )
    argparser.add_argument(
        "-i",
        "--ignorecase",
        help="ignore case of search term",
        action="store_true")
    argparser.add_argument(
        "-l",
        "--line-number",
        help="print line number of each line that contains a match",
        action="store_true",
        dest="linenumber",
        default=True,
    )
    argparser.add_argument(
        "-c",
        "--column",
        help="print column number of each line that contains a match",
        action="store_true",
    )
    argparser.add_argument(
        "-S",
        "--smart-case",
        help="search using smart case (ignore case if all lowercase)",
        action="store_true",
        dest="smartcase",
        default=True,
    )
    argparser.add_argument(
        "--help-types",
        "--list-file-types",
        help="print file types and exit",
        action="store_true",
        dest="helptypes",
    )
    argparser.add_argument(
        "--raw",
        help="don't use HTML formatting when outputing matched lines",
        action="store_true",
    )

    argparser.add_argument(
        "--ruler",
        help="print out a column ruler for each line",
        action="store_true",
    )

    argparser.add_argument("pattern", nargs="?", default="")
    argparser.add_argument("filedirs", nargs="*", default=[os.getcwd()])
    args = argparser.parse_args()

    if args.helptypes:
        with open("types.json", "r") as f:
            types = json.load(f)

            for t in types:
                print(t, ":", types[t])

        sys.exit(1)

    ic(args.filedirs)

    MainWindow = QtWidgets.QMainWindow()

    ui = YapgrepGuiProgram(MainWindow)

    ic(args)
    ui.recursive = args.recurse
    ui.ignorecase = args.ignorecase
    ui.linenumber = args.linenumber
    ui.column = args.column
    ui.smartcase = args.smartcase
    ui.raw = args.raw
    ui.ruler = args.ruler

    ui.ui2.checkBox.setChecked(ui.recursive)
    ui.ui2.checkBox_2.setChecked(ui.ignorecase)
    ui.ui2.checkBox_3.setChecked(ui.linenumber or ui.column)
    ui.ui2.checkBox_4.setChecked(ui.column)
    ui.ui2.checkBox_4.setEnabled(ui.column or ui.linenumber)
    ui.ui2.checkBox_5.setChecked(ui.smartcase)
    ui.ui2.checkBox_6.setChecked(ui.raw)
    ui.ui2.checkBox_7.setChecked(ui.ruler)
    ui.lineEdit.setText(
        QtCore.QCoreApplication.translate("MainWindow",
                                          ":".join(args.filedirs)))
    ui.lineEdit_2.setText(
        QtCore.QCoreApplication.translate("MainWindow", args.pattern))

    MainWindow.show()

    # Read in valid types
    with open("types.json", "r") as f:
        types = json.load(f)

        for t in sorted(types):
            wi = QListWidgetItem(t)
            wi.setCheckState(QtCore.Qt.Unchecked)
            ui.ui2.listWidget.addItem(wi)

    # Find user selected type
    if args.ftype is not None:
        for t in args.ftype:
            if t in types:
                ui.typeList += types[t]
                ic(ui.typeList)
                item = ui.ui2.listWidget.findItems(t, QtCore.Qt.MatchExactly)

                if item:
                    item[0].setCheckState(QtCore.Qt.Checked)
            else:
                msg = "User specified type not found: {}".format(t)
                ic(msg)
                ui.textEdit.append('<font color="red">{}</font>'.format(msg))

    if args.go:
        if len(args.pattern) > 0:
            ui.search()
        else:
            ui.textEdit.append('<font color="red">No pattern specified</font>')

    sys.exit(app.exec_())
