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
        Common.resize(450, 405)
        self.buttonBox = QtWidgets.QDialogButtonBox(Common)
        self.buttonBox.setGeometry(QtCore.QRect(60, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox = QtWidgets.QCheckBox(Common)
        self.checkBox.setGeometry(QtCore.QRect(310, 230, 90, 21))
        self.checkBox.setObjectName("checkBox")
        self.listWidget = QtWidgets.QListWidget(Common)
        self.listWidget.setGeometry(QtCore.QRect(30, 80, 256, 192))
        self.listWidget.setObjectName("listWidget")
        self.checkBox_2 = QtWidgets.QCheckBox(Common)
        self.checkBox_2.setGeometry(QtCore.QRect(310, 180, 131, 21))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(Common)
        self.checkBox_3.setGeometry(QtCore.QRect(310, 30, 131, 27))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(Common)
        self.checkBox_4.setGeometry(QtCore.QRect(310, 80, 95, 27))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(Common)
        self.checkBox_5.setGeometry(QtCore.QRect(310, 130, 121, 27))
        self.checkBox_5.setObjectName("checkBox_5")
        self.label = QtWidgets.QLabel(Common)
        self.label.setGeometry(QtCore.QRect(30, 50, 67, 21))
        self.label.setObjectName("label")
        self.checkBox_6 = QtWidgets.QCheckBox(Common)
        self.checkBox_6.setGeometry(QtCore.QRect(320, 280, 88, 21))
        self.checkBox_6.setObjectName("checkBox_6")

        self.retranslateUi(Common)
        self.buttonBox.accepted.connect(Common.accept)
        self.buttonBox.rejected.connect(Common.reject)
        QtCore.QMetaObject.connectSlotsByName(Common)

    def retranslateUi(self, Common):
        _translate = QtCore.QCoreApplication.translate
        Common.setWindowTitle(_translate("Common", "Dialog"))
        self.checkBox.setText(_translate("Common", "Recurse"))
        self.checkBox_2.setText(_translate("Common", "Ignore Case"))
        self.checkBox_3.setText(_translate("Common", "Line Numbers"))
        self.checkBox_4.setText(_translate("Common", "Column"))
        self.checkBox_5.setText(_translate("Common", "Smart Case"))
        self.label.setText(_translate("Common", "Types"))
        self.checkBox_6.setText(_translate("Common", "Raw"))

