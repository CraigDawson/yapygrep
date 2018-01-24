import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
from yapgrep_gui import Ui_MainWindow
import os
from os.path import join, getsize
import glob
import regex


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
        self.plainTextEdit.clear()
        directory = self.lineEdit.text()
        print('Our Directory from user:', directory)
        try:
            self.wd(directory,regex.compile("for"))
        except:
            print ("some error occurred!", sys.exc_info())
        '''for d in glob.glob(directory):
            self.dbg('d', d)
            if os.path.isdir(d):
                self.walkDir(d,"for")
            else:
                self.plainTextEdit.appendPlainText(d)
                QApplication.instance().processEvents()
        '''
        print("done with walkDir")
        self.statusbar.showMessage('Searching completed.')

        
        '''   def dirWalk(self, directory):
        print('dir: ' + directory)
        try:
            for root, dirs, files in os.walk(directory):
                print(root)
                # print('Dirs: ')
                # print(dirs)
                # print('Files: {}'.format(files))
                # print(root, "consumes", end=" ")
                # print("bytes in", len(files), "non-directory files")
                # print(sum(getsize(join(root, name)) for name in files), end=" ")

                for name in files:
                    self.plainTextEdit.appendPlainText(join(root, name))
                    QApplication.instance().processEvents()
                    
                if '.git' in dirs:
                    dirs.remove('.git')  # don't visit git directories
                    
        except:
            print ("some error occurred!", sys.exc_info()[0])
        '''

    def dbg(self, prefix, item):
        print(prefix + ':', item)
        
    def wd(self, fileSpec, pattern):
        print('walkDir',fileSpec, 'pattern', pattern)
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
            # print('p = ', p)
            if os.path.isfile(p):
                buf = self.grepFile(p, pattern)
                if buf:
                    self.dbg('file', p)
                    print("".join(buf))

        self.dbg('Final fs', fs)


    def grepFile(self, fileName, pattern):
        ''' TODO: save output into buffer and return buffer then in calling
              function, print file name and buffer '''
        buf = []
        with open(fileName, 'r') as f:
            try:
                # print("filename", fileName)
                for i, line in enumerate(f):
                    #print("i, line", i, line)
                    if pattern.match(line):
                        print("  ", i, line, end='')
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
