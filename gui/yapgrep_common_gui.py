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
        self.buttonBox.setGeometry(QtCore.QRect(60, 360, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtWidgets.QListWidget(Common)
        self.listWidget.setGeometry(QtCore.QRect(30, 80, 256, 192))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(Common)
        self.label.setGeometry(QtCore.QRect(30, 50, 67, 21))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(Common)
        self.groupBox.setGeometry(QtCore.QRect(300, 20, 120, 80))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(Common)
        self.layoutWidget.setGeometry(QtCore.QRect(310, 30, 104, 219))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_2.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_2.addWidget(self.checkBox_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_5 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout.addWidget(self.checkBox_5)
        self.checkBox_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_6 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.verticalLayout.addWidget(self.checkBox_6)
        self.checkBox_7 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_7.setObjectName("checkBox_7")
        self.verticalLayout.addWidget(self.checkBox_7)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.groupBox.raise_()
        self.layoutWidget.raise_()
        self.buttonBox.raise_()
        self.listWidget.raise_()
        self.label.raise_()

        self.retranslateUi(Common)
        self.buttonBox.accepted.connect(Common.accept)
        self.buttonBox.rejected.connect(Common.reject)
        QtCore.QMetaObject.connectSlotsByName(Common)

    def retranslateUi(self, Common):
        _translate = QtCore.QCoreApplication.translate
        Common.setWindowTitle(_translate("Common", "Common"))
        self.label.setText(_translate("Common", "Types"))
        self.groupBox.setTitle(_translate("Common", "Numbers"))
        self.checkBox_3.setText(_translate("Common", "Line"))
        self.checkBox_4.setToolTip(_translate("Common", "Column relies on Line numbers"))
        self.checkBox_4.setText(_translate("Common", "Column"))
        self.checkBox_5.setText(_translate("Common", "Smart Case"))
        self.checkBox_2.setText(_translate("Common", "Ignore Case"))
        self.checkBox.setText(_translate("Common", "Recurse"))
        self.checkBox_6.setText(_translate("Common", "Raw"))
        self.checkBox_7.setText(_translate("Common", "Ruler"))

