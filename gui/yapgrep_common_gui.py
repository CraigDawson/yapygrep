# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'common.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Common(object):
    def setupUi(self, Common):
        Common.setObjectName("Common")
        Common.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Common)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox = QtWidgets.QCheckBox(Common)
        self.checkBox.setGeometry(QtCore.QRect(40, 30, 90, 21))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Common)
        self.buttonBox.accepted.connect(Common.accept)
        self.buttonBox.rejected.connect(Common.reject)
        QtCore.QMetaObject.connectSlotsByName(Common)

    def retranslateUi(self, Common):
        _translate = QtCore.QCoreApplication.translate
        Common.setWindowTitle(_translate("Common", "Dialog"))
        self.checkBox.setText(_translate("Common", "Recurse"))
