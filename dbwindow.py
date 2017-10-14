#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Окно редактирования базы данных"""
from PyQt5 import QtWidgets, QtCore, QtSql

import dboperations
from ui.ui_dbwindow import Ui_DBWindow


rus = {
    'transformer': {
        'manufacturer': 'Завод изготовитель',
        'model': 'Модель',
        'nominal_voltage_HV': 'Номинальное напряжение ВН',
        'nominal_voltage_LV': 'Номинальное напряжение НН',
        'connection_windings': 'Схема соединения обмоток',
        'full_rated_capacity': 'Полная номинальная мощность',
        'short_circuit_loss': 'Потери короткого замыкания',
        'impedance_voltage': 'Напряжение короткого замыкания', },
    'cable': {
        'linetype': 'Тип линии',
        'material_of_cable_core': 'Материал жилы кабеля',
        'size_of_cable_phase': 'Сечение фазного проводника, мм2',
        'size_of_cable_neutral': 'Сечение нейтрального проводника, мм2',
        'R1': 'R1',
        'x1': 'X1',
        'R0': 'R0',
        'x0': 'X0', }
}

class DBWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent,
                                   flags=QtCore.Qt.Window)
        self.ui = Ui_DBWindow()
        self.ui.setupUi(self)

        # Установить список таблиц в comboBox_equipment (из базы данных)
        equipment_list = [""]
        equipment_list.extend(list(dboperations.find_tables()))
        equipment_list.sort()
        self.ui.comboBox_equipment.insertItems(0, equipment_list)

        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName("db/database.db")
        self.con.open()

        self.model = None

    @QtCore.pyqtSlot(str)
    def show_equipment_table(self, equipment):
        """Вывод таблицы оборудования"""
        # self.model = QtSql.QSqlQueryModel(parent=self)
        # self.model.setQuery('select * from ' + equipment)
        self.model = QtSql.QSqlTableModel(parent=self)
        self.model.setTable(equipment)
        self.model.setSort(0, QtCore.Qt.AscendingOrder)
        self.model.select()

        field_count = self.model.columnCount()
        for field_index in range(0, field_count):
            field = self.model.record(field_index).fieldName(field_index)
            self.model.setHeaderData(field_index, QtCore.Qt.Horizontal, rus[equipment][field])

        self.ui.tableView.setModel(self.model)
        # self.ui.tableView.hideColumn(0)
        # self.ui.tableView.setColumnWidth(1, 150)
        # self.ui.tableView.setColumnWidth(2, 60)

    @QtCore.pyqtSlot()
    def db_add_equipment(self):
        """Добавление оборудования"""
        self.model.insertRow(self.model.rowCount())

    @QtCore.pyqtSlot()
    def db_copy_equipment(self):
        """Копирование оборудования"""
        pass

    @QtCore.pyqtSlot()
    def db_edit_equipment(self):
        """Редактирование оборудования"""
        pass

    @QtCore.pyqtSlot()
    def db_delete_equipment(self):
        """Удаление оборудования"""
        result = QtWidgets.QMessageBox.warning(self,
                                               "Работа с данными", "Удалить запись?",
                                               buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               defaultButton=QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            self.model.removeRow(self.ui.tableView.currentIndex().row())
            self.model.select()

    def closeEvent(self, e):
        """Обработка события закрытия программы"""
        self.con.close()
        e.accept()
