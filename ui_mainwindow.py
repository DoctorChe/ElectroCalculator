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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(710, 330, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 781, 291))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.lineEdit_B = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_B.setGeometry(QtCore.QRect(30, 40, 113, 20))
        self.lineEdit_B.setObjectName("lineEdit_B")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 51, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 16, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_A = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_A.setGeometry(QtCore.QRect(30, 10, 113, 20))
        self.lineEdit_A.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_A.setObjectName("lineEdit_A")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 31, 16))
        self.label.setObjectName("label")
        self.lineEdit_C = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_C.setGeometry(QtCore.QRect(30, 70, 113, 20))
        self.lineEdit_C.setObjectName("lineEdit_C")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Calculation = QtWidgets.QMenu(self.menubar)
        self.menu_Calculation.setObjectName("menu_Calculation")
        self.menu_Report = QtWidgets.QMenu(self.menubar)
        self.menu_Report.setObjectName("menu_Report")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Calculate = QtWidgets.QAction(MainWindow)
        self.action_Calculate.setObjectName("action_Calculate")
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menu_Calculation.addAction(self.action_Calculate)
        self.menu_Help.addAction(self.action_About)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Calculation.menuAction())
        self.menubar.addAction(self.menu_Report.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label_2.setText(_translate("MainWindow", "B"))
        self.label_3.setText(_translate("MainWindow", "C"))
        self.label.setText(_translate("MainWindow", "A"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menu_File.setTitle(_translate("MainWindow", "&Файл"))
        self.menu_Calculation.setTitle(_translate("MainWindow", "Расчёт"))
        self.menu_Report.setTitle(_translate("MainWindow", "Отчёт"))
        self.menu_Help.setTitle(_translate("MainWindow", "Справка"))
        self.action_Calculate.setText(_translate("MainWindow", "Запустить расчёт"))
        self.action_About.setText(_translate("MainWindow", "О программе..."))
        self.action_Open.setText(_translate("MainWindow", "Открыть"))
        self.action_Save.setText(_translate("MainWindow", "Сохранить"))
        self.action_Exit.setText(_translate("MainWindow", "В&ыход"))

