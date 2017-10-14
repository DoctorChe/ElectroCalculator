#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Диалоговое окно добавления кабеля (воздушной линии, шинопровода)"""
from PyQt5 import QtWidgets, QtCore

import dboperations
from ui.ui_addcabledialog import Ui_AddCableDialog


class AddCableDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent,
                                   flags=QtCore.Qt.Window)
        self.ui = Ui_AddCableDialog()
        self.ui.setupUi(self)

        # Установить список типов линии в comboBox_linetype (из базы данных)
        linetype_list = [""]
        linetype_list.extend(list(dboperations.find_linetypes()))
        linetype_list.sort()
        self.ui.comboBox_linetype.insertItems(0, linetype_list)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_linetype(self, linetype):
        """
        Поиск материалов жил кабеля или марки шинопровода в базе
        Добавление их в comboBox_material_of_cable_core
        """
        material_of_cable_core = dboperations.find_material_of_cable_core(linetype)
        self.ui.comboBox_material_of_cable_core.clear()
        self.ui.comboBox_material_of_cable_core.insertItems(1, material_of_cable_core)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_material_of_cable_core(self, material_of_cable_core):
        """
        Поиск сечений фазных жил кабеля в базе
        Добавление их в comboBox_size_of_cable_phase
        """
        linetype = self.ui.comboBox_linetype.currentText()
        size_of_cable_phase = dboperations.find_size_of_cable_phase(linetype, material_of_cable_core)
        self.ui.comboBox_size_of_cable_phase.clear()
        self.ui.comboBox_size_of_cable_phase.insertItems(0, size_of_cable_phase)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_size_of_cable_phase(self, size_of_cable_phase):
        """
        Поиск сечений нейтральных жил кабеля в базе
        Добавление их в comboBox_size_of_cable_neutral
        """
        linetype = self.ui.comboBox_linetype.currentText()
        material_of_cable_core = self.ui.comboBox_material_of_cable_core.currentText()
        size_of_cable_neutral = dboperations.find_size_of_cable_neutral(linetype, material_of_cable_core,
                                                                        size_of_cable_phase)
        self.ui.comboBox_size_of_cable_neutral.clear()
        self.ui.comboBox_size_of_cable_neutral.insertItems(0, size_of_cable_neutral)

# TODO Сделать проверку на введение всех данных перед нажатием кнопки OK
# TODO Расчёт начальной температуры кабеля
