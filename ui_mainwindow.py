# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 16, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_B = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_B.setGeometry(QtCore.QRect(30, 40, 113, 20))
        self.lineEdit_B.setObjectName("lineEdit_B")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 51, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit_A = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_A.setGeometry(QtCore.QRect(30, 10, 113, 20))
        self.lineEdit_A.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_A.setObjectName("lineEdit_A")
        self.lineEdit_C = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_C.setGeometry(QtCore.QRect(30, 70, 113, 20))
        self.lineEdit_C.setObjectName("lineEdit_C")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 31, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "C"))
        self.label_2.setText(_translate("MainWindow", "B"))
        self.label.setText(_translate("MainWindow", "A"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
