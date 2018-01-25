import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
from yapgrep_gui import Ui_MainWindow
import os
from os.path import join, getsize
import glob
import regex
import time


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
        self.files = 0
        self.matches = 0
        self.statusbar.showMessage('Searching . . .')
        self.plainTextEdit.clear()
        directory = self.lineEdit.text()
        print('Directory from user:', directory)
        try:
            self.wd(directory,regex.compile("for"))
        except:
            print ("some error occurred!", sys.exc_info())
        
        self.statusbar.showMessage('Searching completed.')

    def dbg(self, prefix, item):
        print(prefix + ':', item)
        
    def wd(self, fileSpec, pattern):
        fs = os.path.expanduser(fileSpec)
        self.dbg('fs/expanduser', fs)

        fs = os.path.expandvars(fs)
        self.dbg('fs/expandvars', fs)

        if os.path.isdir(fs):
            self.dbg('fs', 'adding "/**" to dir')
            fs += '/**'
        # Not dir and no wildcard at end then append '**' ???
        #elif not fs.endswith('*'):
        #    fs += '**'

        base = os.path.basename(fs)
        self.dbg('base', base)

        path = os.path.dirname(fs)
        self.dbg('path', path)

        for p in glob.iglob(fs, recursive=True):
            if os.path.isfile(p):
                buf = self.grepFile(p, pattern)
                if buf:
                    self.dbg('file', p)
                    print("".join(buf))

        self.dbg('Final fs', fs)
        print('Files searched: {}, Matches found: {}'.format(self.files, self.matches))


    def grepFile(self, fileName, pattern):
        ''' TODO: save output into buffer and return buffer then in calling
              function, print file name and buffer '''
        buf = []
        with open(fileName, 'r') as f:
            try:
                self.files += 1
                self.statusbar.showMessage(fileName)
                #time.sleep(1)
                for i, line in enumerate(f):
                    if pattern.match(line):
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
