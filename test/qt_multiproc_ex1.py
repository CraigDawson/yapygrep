import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import multiprocessing as mp
import numpy

import better_exceptions


class WorkThread(QThread):
    finished = pyqtSignal(int, object)

    def __del__(self):
        self.wait()

    def cube(self, x):
        return x, x**3

    def run(self):
        aa = numpy.random.rand(4, 2, 3)

        pool = mp.Pool(processes=4)
        results = [pool.apply_async(self.cube, args=(aa[:, :, x],)) for x in range(0, aa.shape[2])]
        output = [p.get() for p in results]
        test_va = numpy.asarray(output)

        for i in range(5):

            QThread.sleep(0.3)  # artificial time delay

            self.finished.emit(i, test_va)


class test_multicore(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 280, 600)
        self.setWindowTitle('Qthreads and multicore')

        self.layout = QVBoxLayout(self)

        self.testButton = QPushButton("test")
        self.testButton.clicked.connect(self.test)

        self.listwidget = QListWidget(self)

        self.layout.addWidget(self.testButton)
        self.layout.addWidget(self.listwidget)
        self.threadPool = []

    def add(self, text, random_matrix):
        """ Add item to list widget """
        print("Add: " + str(text) + str(random_matrix))
        self.listwidget.addItem(str(text))
        self.listwidget.sortItems()

    def addBatch(self, text="text", iters=6, delay=0.3):
        """ Add several items to list widget """
        for i in range(iters):
            time.sleep(delay)  # artificial time delay
            self.add(text + " " + str(i), 0)

    def test(self):
        self.listwidget.clear()

        self.addBatch("_non_thread_entries", iters=6, delay=0.3)

        self.workThread = WorkThread()
        self.workThread.finished[int, object].connect(self.add)

        self.workThread.start()


# run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = test_multicore()
    test.show()
    app.exec_()
