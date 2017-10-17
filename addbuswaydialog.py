#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Диалоговое окно добавления кабеля (воздушной линии, шинопровода)"""
from PyQt5 import QtWidgets, QtCore

import dboperations
from ui.ui_addbuswaydialog import  Ui_AddBuswayDialog


class AddBuswayDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent,
                                   flags=QtCore.Qt.Window)
        self.ui = Ui_AddBuswayDialog()
        self.ui.setupUi(self)

        # Установить список типов линии в comboBox_linetype (из базы данных)
        linetype_list = [""]
        linetype_list.extend(list(dboperations.find_busway_manufactures()))
        linetype_list.sort()
        self.ui.comboBox_linetype.insertItems(0, linetype_list)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_linetype(self, linetype):
        """
        Поиск материалов жил кабеля или марки шинопровода в базе
        Добавление их в comboBox_material_of_cable_core
        """
        material_of_cable_core = dboperations.find_busway_model(linetype)
        self.ui.comboBox_material_of_cable_core.clear()
        if len(material_of_cable_core) > 1:
            self.ui.comboBox_material_of_cable_core.insertItems(0, ['',])
        self.ui.comboBox_material_of_cable_core.insertItems(1, material_of_cable_core)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_material_of_cable_core(self, material_of_cable_core):
        """
        Поиск сечений фазных жил кабеля в базе
        Добавление их в comboBox_size_of_cable_phase
        """
        linetype = self.ui.comboBox_linetype.currentText()
        size_of_cable_phase = dboperations.find_busway_rated_current(linetype, material_of_cable_core)
        size_of_cable_phase = AddBuswayDialog.filterbyvalue(size_of_cable_phase, -1)
        self.ui.comboBox_size_of_cable_phase.clear()
        if len(size_of_cable_phase) > 1:
            self.ui.comboBox_size_of_cable_phase.insertItems(0, ['',])
        self.ui.comboBox_size_of_cable_phase.insertItems(1, size_of_cable_phase)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_size_of_cable_phase(self, size_of_cable_phase):
        """
        Поиск сечений нейтральных жил кабеля в базе
        Добавление их в comboBox_size_of_cable_neutral
        """
        linetype = self.ui.comboBox_linetype.currentText()
        material_of_cable_core = self.ui.comboBox_material_of_cable_core.currentText()
        size_of_cable_neutral = dboperations.find_busway_material(linetype, material_of_cable_core,
                                                                        size_of_cable_phase)
        # size_of_cable_neutral = AddBuswayDialog.filterbyvalue(size_of_cable_neutral, -1)
        self.ui.comboBox_size_of_cable_neutral.clear()
        if len(size_of_cable_neutral) > 1:
            self.ui.comboBox_size_of_cable_neutral.insertItems(0, ['',])
        self.ui.comboBox_size_of_cable_neutral.insertItems(1, size_of_cable_neutral)

    @staticmethod
    def filterbyvalue(my_list, value):
        res = []
        for i, elem in enumerate(my_list):
            if elem == value:
                res.append('нет')
            else:
                res.append(str(elem))
        return res

    def accept(self):
        if self.ui.comboBox_linetype.currentText() == "":
            QtWidgets.QMessageBox.information(self, "Предупреждение",
                                              "Не задан тип линии",
                                              buttons=QtWidgets.QMessageBox.Close,
                                              defaultButton=QtWidgets.QMessageBox.Close)
        elif self.ui.comboBox_material_of_cable_core.currentText() == "":
            QtWidgets.QMessageBox.information(self, "Предупреждение",
                                              "Не задан материал жилы или марка шинопровода",
                                              buttons=QtWidgets.QMessageBox.Close,
                                              defaultButton=QtWidgets.QMessageBox.Close)
        elif self.ui.doubleSpinBox_linelength.value() == 0:
            QtWidgets.QMessageBox.information(self, "Предупреждение",
                                              "Заданная длина линии равна 0 м",
                                              buttons=QtWidgets.QMessageBox.Close,
                                              defaultButton=QtWidgets.QMessageBox.Close)
        elif self.ui.comboBox_size_of_cable_phase.currentText() == "":
            QtWidgets.QMessageBox.information(self, "Предупреждение",
                                              "Не задано сечение фазного проводника",
                                              buttons=QtWidgets.QMessageBox.Close,
                                              defaultButton=QtWidgets.QMessageBox.Close)
        elif self.ui.comboBox_size_of_cable_neutral.currentText() == "":
            QtWidgets.QMessageBox.information(self, "Предупреждение",
                                              "Не задано сечение нулевого проводника",
                                              buttons=QtWidgets.QMessageBox.Close,
                                              defaultButton=QtWidgets.QMessageBox.Close)
        else:
            super().accept()

# TODO Расчёт начальной температуры кабеля
# TODO Добавление в базу данных - добавить возможность копирования записи с последующим редактированием
# TODO Добавление в базу данных - проверка на заполнение всех полей перед добавлением
# TODO Добавление в базу данных - проверка на наличие аналогичных записей перед добавлением
