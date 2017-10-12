# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_addcabledialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddCableDialog(object):
    def setupUi(self, AddCableDialog):
        AddCableDialog.setObjectName("AddCableDialog")
        AddCableDialog.resize(649, 392)
        AddCableDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(AddCableDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(AddCableDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(AddCableDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(AddCableDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(AddCableDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.comboBox_size_of_cable_phase = QtWidgets.QComboBox(AddCableDialog)
        self.comboBox_size_of_cable_phase.setObjectName("comboBox_size_of_cable_phase")
        self.gridLayout.addWidget(self.comboBox_size_of_cable_phase, 5, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(AddCableDialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.spinBox_temperature = QtWidgets.QSpinBox(AddCableDialog)
        self.spinBox_temperature.setMaximum(9999)
        self.spinBox_temperature.setProperty("value", 20)
        self.spinBox_temperature.setObjectName("spinBox_temperature")
        self.gridLayout.addWidget(self.spinBox_temperature, 7, 2, 1, 1)
        self.comboBox_linetype = QtWidgets.QComboBox(AddCableDialog)
        self.comboBox_linetype.setObjectName("comboBox_linetype")
        self.gridLayout.addWidget(self.comboBox_linetype, 1, 2, 1, 2)
        self.comboBox_material_of_cable_core = QtWidgets.QComboBox(AddCableDialog)
        self.comboBox_material_of_cable_core.setObjectName("comboBox_material_of_cable_core")
        self.gridLayout.addWidget(self.comboBox_material_of_cable_core, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(AddCableDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBox_parallel_fider = QtWidgets.QSpinBox(AddCableDialog)
        self.spinBox_parallel_fider.setMinimum(1)
        self.spinBox_parallel_fider.setObjectName("spinBox_parallel_fider")
        self.gridLayout.addWidget(self.spinBox_parallel_fider, 4, 2, 1, 1)
        self.comboBox_size_of_cable_neutral = QtWidgets.QComboBox(AddCableDialog)
        self.comboBox_size_of_cable_neutral.setObjectName("comboBox_size_of_cable_neutral")
        self.gridLayout.addWidget(self.comboBox_size_of_cable_neutral, 6, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(AddCableDialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.toolButton = QtWidgets.QToolButton(AddCableDialog)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 7, 3, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddCableDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 2, 1, 2)
        self.label = QtWidgets.QLabel(AddCableDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.doubleSpinBox_linelength = QtWidgets.QDoubleSpinBox(AddCableDialog)
        self.doubleSpinBox_linelength.setObjectName("doubleSpinBox_linelength")
        self.gridLayout.addWidget(self.doubleSpinBox_linelength, 3, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(AddCableDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.retranslateUi(AddCableDialog)
        self.buttonBox.accepted.connect(AddCableDialog.accept)
        self.buttonBox.rejected.connect(AddCableDialog.reject)
        self.comboBox_linetype.currentTextChanged['QString'].connect(AddCableDialog.on_clicked_comboBox_linetype)
        self.comboBox_material_of_cable_core.currentTextChanged['QString'].connect(AddCableDialog.on_clicked_comboBox_material_of_cable_core)
        self.comboBox_size_of_cable_phase.currentTextChanged['QString'].connect(AddCableDialog.on_clicked_comboBox_size_of_cable_phase)
        QtCore.QMetaObject.connectSlotsByName(AddCableDialog)

    def retranslateUi(self, AddCableDialog):
        _translate = QtCore.QCoreApplication.translate
        AddCableDialog.setWindowTitle(_translate("AddCableDialog", "Диалог добавления линии"))
        self.label_2.setText(_translate("AddCableDialog", "Тип линии"))
        self.label_4.setText(_translate("AddCableDialog", "Длина линии, м"))
        self.label_6.setText(_translate("AddCableDialog", "Сечение фазного проводника, мм²"))
        self.label_7.setText(_translate("AddCableDialog", "Сечение нулевого проводника, мм²"))
        self.label_3.setText(_translate("AddCableDialog", "Материал жилы или марка шинопровода"))
        self.label_8.setText(_translate("AddCableDialog", "Начальная температура проводника, °С"))
        self.toolButton.setText(_translate("AddCableDialog", "..."))
        self.label.setText(_translate("AddCableDialog", "Маркировка линии"))
        self.label_5.setText(_translate("AddCableDialog", "Количество параллельных проводников, шт."))

