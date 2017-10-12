# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dbwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DBWindow(object):
    def setupUi(self, DBWindow):
        DBWindow.setObjectName("DBWindow")
        DBWindow.resize(832, 409)
        DBWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        DBWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DBWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(DBWindow)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_equipment = QtWidgets.QComboBox(DBWindow)
        self.comboBox_equipment.setObjectName("comboBox_equipment")
        self.horizontalLayout.addWidget(self.comboBox_equipment)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView = QtWidgets.QTableView(DBWindow)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(DBWindow)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(DBWindow)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(DBWindow)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(DBWindow)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton_close = QtWidgets.QPushButton(DBWindow)
        self.pushButton_close.setObjectName("pushButton_close")
        self.verticalLayout.addWidget(self.pushButton_close, 0, QtCore.Qt.AlignRight)

        self.retranslateUi(DBWindow)
        self.comboBox_equipment.currentTextChanged['QString'].connect(DBWindow.show_equipment_table)
        self.pushButton.clicked.connect(DBWindow.db_add_equipment)
        self.pushButton_2.clicked.connect(DBWindow.db_copy_equipment)
        self.pushButton_3.clicked.connect(DBWindow.db_edit_equipment)
        self.pushButton_4.clicked.connect(DBWindow.db_delete_equipment)
        self.pushButton_close.clicked.connect(DBWindow.close)
        QtCore.QMetaObject.connectSlotsByName(DBWindow)

    def retranslateUi(self, DBWindow):
        _translate = QtCore.QCoreApplication.translate
        DBWindow.setWindowTitle(_translate("DBWindow", "База данных"))
        self.label.setText(_translate("DBWindow", "Выберите необходимый тип оборудование из списка"))
        self.pushButton.setText(_translate("DBWindow", "Добавить"))
        self.pushButton_2.setText(_translate("DBWindow", "Копировать"))
        self.pushButton_3.setText(_translate("DBWindow", "Редактировать"))
        self.pushButton_4.setText(_translate("DBWindow", "Удалить"))
        self.pushButton_close.setText(_translate("DBWindow", "Закрыть"))

