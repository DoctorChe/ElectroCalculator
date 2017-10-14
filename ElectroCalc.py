#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Программа для вычисления токов короткого замыкания"""

import sys
# Импортируем наш интерфейс из файла
from ui.ui_mainwindow import Ui_MainWindow
# from PyQt5 import uic
# from PyQt5.uic import loadUi
# from short_circuit_current_calculation import calc_Ip0_3ph
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
# from PyQt5.QtWidgets import QAction
import short_circuit_current_calculation as sccc
import dboperations
import addcabledialog
import dbwindow
import math

from appy.pod.renderer import Renderer

tr_connection_windings_list = ["Y/Yн-0", "Yн/Y-0", "Y/Δ-11", "Yн/Δ-11", "Y/Zн-11", "Δ/Yн-11", "Δ/Δ-0", "1/1н"]


# class MyWin(QtWidgets.QMainWindow):
class MyWin(QMainWindow):
    """
    Основной класс программы
    """

    def __init__(self, iniFile, parent=None):
        # QtWidgets.QWidget.__init__(self, parent)
        # QWidget.__init__(self, parent)
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dbwindow = None
        # self.ui = loadUi('ui_mainwindow.ui', self)
        self.iniFile = iniFile
        self.settings = QtCore.QSettings(iniFile, QtCore.QSettings.IniFormat)
        self.settings.setIniCodec("utf-8")

        # Установить список производителей трансформаторов в comboBox_tr_manufacturer (из базы данных)
        manufactures_list = [""]
        manufactures_list.extend(list(dboperations.find_manufacturers()))
        manufactures_list.sort()
        self.ui.comboBox_tr_manufacturer.insertItems(0, manufactures_list)

        # Чтение настроек
        self.read_settings()

        # Событие - запуск вычисления
        self.ui.action_Calculate.triggered.connect(self.my_function)

        # Событие - выход из программы
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_About.triggered.connect(self.show_about_window)
        self.ui.action_Qt.triggered.connect(self.show_aboutqt_window)

        self.ui.action_ODT.triggered.connect(self.save_report_odt)

        self.ui.action_Open.triggered.connect(self.open_file_dialog)
        self.ui.action_Save.triggered.connect(self.save_file_dialog)

        self.ui.action_db.triggered.connect(self.show_db_window)

        # Здесь прописываем событие нажатия на кнопку
        # self.ui.pushButton.clicked.connect(self.my_function)

        # self.ui.pushButton.clicked.connect(self.ui.action_Exit)
        # self.ui.pushButton.addAction(self.ui.action_Exit)

        # self.ui.lineEdit.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))

        # Событие - выбор параметра режима тр-ра
        # self.ui.comboBox_tr_regime.currentIndexChanged.connect(self.on_clicked_comboBox_tr_regime)
        # self.ui.comboBox_tr_regime_value.hide()
        # self.ui.comboBox_tr_regime_value.setCurrentIndex(2)
        #        self.ui.comboBox_tr_regime.activated.connect(self.on_clicked_comboBox_tr_regime)

        # self.ui.comboBox_tr_manufacturer.activated[str].connect(self.on_clicked_comboBox_tr_manufacturer)

        # Регулярное выражение для валидатора
        self.v = QRV("^([1-9][0-9]*|0)(\\.|,)[0-9]{4}")
        # Установка валидатора на поля ввода
        self.ui.lineEdit_Sk_IkVN_Xs.setValidator(self.v)
        self.ui.comboBox_U_sr_VN.setValidator(self.v)
        self.ui.comboBox_U_sr_NN.setValidator(self.v)
        self.ui.comboBox_tr_full_rated_capacity.setValidator(self.v)
        self.ui.comboBox_tr_short_circuit_loss.setValidator(self.v)
        self.ui.comboBox_tr_impedance_voltage.setValidator(self.v)
        self.ui.lineEdit_tr_regime_value.setValidator(self.v)
        self.ui.lineEdit_Rt.setValidator(self.v)
        self.ui.lineEdit_Xt.setValidator(self.v)
        self.ui.lineEdit_R0t.setValidator(self.v)
        self.ui.lineEdit_X0t.setValidator(self.v)
        self.ui.lineEdit_Rsh.setValidator(self.v)
        self.ui.lineEdit_Xsh.setValidator(self.v)
        self.ui.lineEdit_R0sh.setValidator(self.v)
        self.ui.lineEdit_X0sh.setValidator(self.v)
        self.ui.lineEdit_R_1kb.setValidator(self.v)
        self.ui.lineEdit_X_1kb.setValidator(self.v)
        self.ui.lineEdit_R_0kb.setValidator(self.v)
        self.ui.lineEdit_X_0kb.setValidator(self.v)
        self.ui.lineEdit_Rvl.setValidator(self.v)
        self.ui.lineEdit_Xvl.setValidator(self.v)
        self.ui.lineEdit_R0vl.setValidator(self.v)
        self.ui.lineEdit_X0vl.setValidator(self.v)
        self.ui.lineEdit_Rr.setValidator(self.v)
        self.ui.lineEdit_Xr.setValidator(self.v)
        self.ui.lineEdit_Rk.setValidator(self.v)
        self.ui.lineEdit_Rkv.setValidator(self.v)
        self.ui.lineEdit_Xkv.setValidator(self.v)
        self.ui.lineEdit_Rta.setValidator(self.v)
        self.ui.lineEdit_Xta.setValidator(self.v)
        self.ui.lineEdit_Rd.setValidator(self.v)

    @QtCore.pyqtSlot(int)
    def on_clicked_comboBox_tr_regime(self, index):
        """
        Переключение режима трасформатора
        """
        if not index:
            self.ui.comboBox_tr_regime_value.hide()
            self.ui.lineEdit_tr_regime_value.show()
        else:
            self.ui.comboBox_tr_regime_value.show()
            self.ui.lineEdit_tr_regime_value.hide()

    @QtCore.pyqtSlot()
    def update_comboBox_tr_manufacturer(self):
        """
        Поиск заводов-производителей трансформаторов в базе
        Добавление их в comboBox_tr_manufacturer
        """
        models = dboperations.find_manufacturers()
        # self.ui.comboBox_tr_manufacturer.clear()
        self.ui.comboBox_tr_manufacturer.insertItems(1, models)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_tr_manufacturer(self, manufacturer):
        """
        Поиск моделей трансформаторов в базе
        Добавление их в comboBox_tr_model
        """
        models = dboperations.find_models(manufacturer)
        self.ui.comboBox_tr_model.clear()
        self.ui.comboBox_tr_model.insertItems(0, models)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_tr_model(self, model):
        """
        Поиск номинальных напряжений ВН трансформаторов в базе
        Добавление их в comboBox_U_sr_VN
        """
        manufacturer = self.ui.comboBox_tr_manufacturer.currentText()
        nominal_voltage_HV = dboperations.find_nominal_voltage_HV(manufacturer, model)
        self.ui.comboBox_U_sr_VN.clear()
        self.ui.comboBox_U_sr_VN.insertItems(0, nominal_voltage_HV)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_U_sr_VN(self, nominal_voltage_HV):
        """
        Поиск номинальных напряжений НН трансформаторов в базе
        Добавление их в comboBox_U_sr_NN
        """
        manufacturer = self.ui.comboBox_tr_manufacturer.currentText()
        model = self.ui.comboBox_tr_model.currentText()
        nominal_voltage_LV = dboperations.find_nominal_voltage_LV(manufacturer, model, nominal_voltage_HV)
        self.ui.comboBox_U_sr_NN.clear()
        self.ui.comboBox_U_sr_NN.insertItems(0, nominal_voltage_LV)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_U_sr_NN(self, nominal_voltage_LV):
        """
        Поиск схем соединений обмоток трансформаторов в базе
        Добавление их в comboBox_tr_connection_windings
        """
        manufacturer = self.ui.comboBox_tr_manufacturer.currentText()
        model = self.ui.comboBox_tr_model.currentText()
        nominal_voltage_HV = self.ui.comboBox_U_sr_VN.currentText()
        connection_windings = dboperations.find_connection_windings(manufacturer, model,
                                                                    nominal_voltage_HV, nominal_voltage_LV)
        self.ui.comboBox_tr_connection_windings.clear()
        self.ui.comboBox_tr_connection_windings.insertItems(0, connection_windings)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_tr_connection_windings(self, connection_windings):
        """
        Поиск полных номинальных мощностей трансформаторов в базе
        Добавление их в comboBox_tr_full_rated_capacity
        """
        manufacturer = self.ui.comboBox_tr_manufacturer.currentText()
        model = self.ui.comboBox_tr_model.currentText()
        nominal_voltage_HV = self.ui.comboBox_U_sr_VN.currentText()
        nominal_voltage_LV = self.ui.comboBox_U_sr_NN.currentText()
        full_rated_capacity = dboperations.find_full_rated_capacity(manufacturer, model, nominal_voltage_HV,
                                                                    nominal_voltage_LV, connection_windings)
        self.ui.comboBox_tr_full_rated_capacity.clear()
        self.ui.comboBox_tr_full_rated_capacity.insertItems(0, full_rated_capacity)
        # self.ui.comboBox_tr_full_rated_capacity.view().model().sort(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_tr_full_rated_capacity(self, full_rated_capacity):
        """
        Поиск потерь короткого замыкания трансформаторов в базе
        Добавление их в comboBox_tr_short_circuit_loss
        """
        manufacturer = self.ui.comboBox_tr_manufacturer.currentText()
        model = self.ui.comboBox_tr_model.currentText()
        nominal_voltage_HV = self.ui.comboBox_U_sr_VN.currentText()
        nominal_voltage_LV = self.ui.comboBox_U_sr_NN.currentText()
        connection_windings = self.ui.comboBox_tr_connection_windings.currentText()
        short_circuit_loss = dboperations.find_short_circuit_loss(manufacturer, model, nominal_voltage_HV,
                                                                  nominal_voltage_LV, connection_windings,
                                                                  full_rated_capacity)
        self.ui.comboBox_tr_short_circuit_loss.clear()
        self.ui.comboBox_tr_short_circuit_loss.insertItems(0, short_circuit_loss)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_tr_short_circuit_loss(self, short_circuit_loss):
        """
        Поиск напряжений короткого замыкания трансформаторов в базе
        Добавление их в comboBox_tr_impedance_voltage
        """
        manufacturer = self.ui.comboBox_tr_manufacturer.currentText()
        model = self.ui.comboBox_tr_model.currentText()
        nominal_voltage_HV = self.ui.comboBox_U_sr_VN.currentText()
        nominal_voltage_LV = self.ui.comboBox_U_sr_NN.currentText()
        connection_windings = self.ui.comboBox_tr_connection_windings.currentText()
        full_rated_capacity = self.ui.comboBox_tr_full_rated_capacity.currentText()
        impedance_voltage = dboperations.find_impedance_voltage(manufacturer, model, nominal_voltage_HV,
                                                                nominal_voltage_LV, connection_windings,
                                                                full_rated_capacity, short_circuit_loss)
        self.ui.comboBox_tr_impedance_voltage.clear()
        self.ui.comboBox_tr_impedance_voltage.insertItems(0, impedance_voltage)

    def calc_tr_data(self):
        # Считывание данных трансформатора
        try:
            # Параметры трансформатора
            St_nom = 1
            U_NN_nom = 0
            Pk_nom = 0
            u_k = 0
            R0t = 0
            X0t = 0
            St_nom = float(self.ui.comboBox_tr_full_rated_capacity.currentText())
            U_NN_nom = float(self.ui.comboBox_U_sr_NN.currentText())
            Pk_nom = float(self.ui.comboBox_tr_short_circuit_loss.currentText())
            u_k = float(self.ui.comboBox_tr_impedance_voltage.currentText())
            # R0t = float(self.ui.lineEdit_R0t.text())
            # X0t = float(self.ui.lineEdit_X0t.text())
        except ValueError:
            msg = ("Исходные данные трансформатора введены не корректно. " +
                   "Сопротивление трансформатора в расчётах не учитывается.")
            self.statusBar().showMessage(msg)
        else:
            # Pk_nom, U_NN_nom, St_nom, u_k, R0t, X0t,  # Трансформатор
            R1t = sccc.calc_Rt(Pk_nom, U_NN_nom, St_nom)
            X1t = sccc.calc_Xt(Pk_nom, U_NN_nom, St_nom, u_k)
            self.ui.lineEdit_Rt.setText("{:.2f}".format(R1t))
            self.ui.lineEdit_Xt.setText("{:.2f}".format(X1t))
            if self.ui.comboBox_tr_connection_windings.currentText() == "Δ/Yн-11":
                R0t = R1t
                X0t = X1t
                self.ui.lineEdit_R0t.setText("{:.2f}".format(R0t))
                self.ui.lineEdit_X0t.setText("{:.2f}".format(X0t))
                msg = "Расчетные данные трансформатора вычислены успешно."
                self.statusBar().showMessage(msg)
            else:
                self.ui.lineEdit_R0t.setText("")
                self.ui.lineEdit_X0t.setText("")
                msg = "Введите сопротивление нулевой последовательности трансформатора вручную."
                self.statusBar().showMessage(msg)

    def checked_radioButton_tr_from_db(self):
        self.ui.comboBox_tr_manufacturer.blockSignals(False)
        self.ui.comboBox_tr_model.blockSignals(False)
        self.ui.comboBox_U_sr_VN.blockSignals(False)
        self.ui.comboBox_U_sr_NN.blockSignals(False)
        self.ui.comboBox_tr_connection_windings.blockSignals(False)
        self.ui.comboBox_tr_full_rated_capacity.blockSignals(False)
        self.ui.comboBox_tr_impedance_voltage.blockSignals(False)
        self.ui.comboBox_tr_short_circuit_loss.blockSignals(False)
        self.ui.comboBox_tr_manufacturer.setEditable(False)
        self.ui.comboBox_tr_model.setEditable(False)
        self.ui.comboBox_U_sr_VN.setEditable(False)
        self.ui.comboBox_U_sr_NN.setEditable(False)
        self.ui.comboBox_tr_connection_windings.setEditable(False)
        self.ui.comboBox_tr_full_rated_capacity.setEditable(False)
        self.ui.comboBox_tr_impedance_voltage.setEditable(False)
        self.ui.comboBox_tr_short_circuit_loss.setEditable(False)
        self.ui.comboBox_tr_manufacturer.setCurrentIndex(0)

    def checked_radioButton_tr_manual(self):
        self.ui.comboBox_tr_manufacturer.blockSignals(True)
        self.ui.comboBox_tr_model.blockSignals(True)
        self.ui.comboBox_U_sr_VN.blockSignals(True)
        self.ui.comboBox_U_sr_NN.blockSignals(True)
        self.ui.comboBox_tr_connection_windings.blockSignals(True)
        self.ui.comboBox_tr_full_rated_capacity.blockSignals(True)
        self.ui.comboBox_tr_impedance_voltage.blockSignals(True)
        self.ui.comboBox_tr_short_circuit_loss.blockSignals(True)
        self.ui.comboBox_U_sr_VN.clear()
        self.ui.comboBox_U_sr_NN.clear()
        self.ui.comboBox_tr_connection_windings.clear()
        self.ui.comboBox_tr_connection_windings.insertItems(0, ("", ))
        self.ui.comboBox_tr_connection_windings.insertItems(1, tr_connection_windings_list)
        self.ui.comboBox_tr_full_rated_capacity.clear()
        self.ui.comboBox_tr_impedance_voltage.clear()
        self.ui.comboBox_tr_short_circuit_loss.clear()
        self.ui.comboBox_U_sr_VN.setEditable(True)
        self.ui.comboBox_U_sr_NN.setEditable(True)
        # self.ui.comboBox_tr_connection_windings.setEditable(True)
        self.ui.comboBox_tr_full_rated_capacity.setEditable(True)
        self.ui.comboBox_tr_impedance_voltage.setEditable(True)
        self.ui.comboBox_tr_short_circuit_loss.setEditable(True)

    def closeEvent(self, e):  # pylint: disable=invalid-name
        """Обработка события закрытия программы"""
        # Write data to config file
        # if not self.iniFile == "last_values.ini":
        #     self.iniFile = "last_values.ini"
        self.settings = QtCore.QSettings(self.iniFile, QtCore.QSettings.IniFormat)
        self.settings.setIniCodec("utf-8")
        self.save_settings()
        e.accept()

    def read_settings(self):
        """Чтение настроек"""
        #        self.inputs = {}
        #        self.params = []
        #        ini.beginGroup("Common")
        #        wt = ini.value('Title','')
        #        if wt != '': self.setWindowTitle(wt)
        #        ini.endGroup()

        #        chBoxState = settings.value('chBoxState', QtCore.Qt.Checked)
        #        self.chB.setCheckState(int(chBoxState))

        self.settings.beginGroup("Transformer")
        check_state = self.settings.value("tr_from_db", False, type=bool)
        self.ui.radioButton_tr_from_db.setChecked(check_state)
        self.ui.radioButton_tr_manual.setChecked(not check_state)
        self.ui.comboBox_tr_manufacturer.setCurrentText(self.settings.value("tr_manufacturer"))
        self.ui.comboBox_tr_model.setCurrentText(self.settings.value("tr_model"))
        self.ui.comboBox_U_sr_VN.setCurrentText(self.settings.value("U_sr_VN", 10))
        self.ui.comboBox_U_sr_NN.setCurrentText(self.settings.value("U_sr_NN", 400))
        self.ui.comboBox_tr_connection_windings.setCurrentText(self.settings.value("tr_connection_windings"))
        self.ui.comboBox_tr_full_rated_capacity.setCurrentText(self.settings.value("tr_full_rated_capacity"))
        self.ui.comboBox_tr_short_circuit_loss.setCurrentText(self.settings.value("tr_short_circuit_loss"))
        self.ui.comboBox_tr_impedance_voltage.setCurrentText(self.settings.value("tr_impedance_voltage"))
        self.ui.lineEdit_Rt.setText(str(self.settings.value("Rt", 0)))
        self.ui.lineEdit_Xt.setText(str(self.settings.value("Xt", 0)))
        self.ui.lineEdit_R0t.setText(str(self.settings.value("R0t", 0)))
        self.ui.lineEdit_X0t.setText(str(self.settings.value("X0t", 0)))
        self.settings.endGroup()

        self.settings.beginGroup("3ph_short_circuit_current_HV")
        self.ui.lineEdit_Sk_IkVN_Xs.setText(str(self.settings.value("Sk_IkVN_Xs_Iotklnom", 0)))
        self.ui.comboBox_Sk_IkVN_Xs.setCurrentIndex(int(self.settings.value("xc_mode", 2)))
        self.settings.endGroup()

        self.settings.beginGroup("Line")
        self.ui.lineEdit_Rsh.setText(str(self.settings.value("Rsh", 0)))
        self.ui.lineEdit_Xsh.setText(str(self.settings.value("Xsh", 0)))
        self.ui.lineEdit_R_1kb.setText(str(self.settings.value("R_1kb", 0)))
        self.ui.lineEdit_X_1kb.setText(str(self.settings.value("X_1kb", 0)))
        self.ui.lineEdit_Rvl.setText(str(self.settings.value("Rvl", 0)))
        self.ui.lineEdit_Xvl.setText(str(self.settings.value("Xvl", 0)))
        self.ui.lineEdit_R0sh.setText(str(self.settings.value("R0sh", 0)))
        self.ui.lineEdit_X0sh.setText(str(self.settings.value("X0sh", 0)))
        self.ui.lineEdit_R_0kb.setText(str(self.settings.value("R_0kb", 0)))
        self.ui.lineEdit_X_0kb.setText(str(self.settings.value("X_0kb", 0)))
        self.ui.lineEdit_R0vl.setText(str(self.settings.value("R0vl", 0)))
        self.ui.lineEdit_X0vl.setText(str(self.settings.value("X0vl", 0)))
        self.settings.endGroup()

        self.settings.beginGroup("Other_circuit_elements")
        self.ui.tabWidget_2.setCurrentIndex(int(self.settings.value("Other_circuit_elements_tab", 0)))
        self.ui.lineEdit_Rpr.setText(str(self.settings.value("Rpr", 0)))
        self.ui.lineEdit_Xpr.setText(str(self.settings.value("Xpr", 0)))
        self.ui.lineEdit_Rr.setText(str(self.settings.value("Rr", 0)))
        self.ui.lineEdit_Xr.setText(str(self.settings.value("Xr", 0)))
        self.ui.lineEdit_Rk.setText(str(self.settings.value("Rk", 0)))
        self.ui.lineEdit_Rkv.setText(str(self.settings.value("Rkv", 0)))
        self.ui.lineEdit_Xkv.setText(str(self.settings.value("Xkv", 0)))
        self.ui.lineEdit_Rta.setText(str(self.settings.value("Rta", 0)))
        self.ui.lineEdit_Xta.setText(str(self.settings.value("Xta", 0)))
        self.ui.lineEdit_Rd.setText(str(self.settings.value("Rd", 0)))
        self.settings.endGroup()

    def save_settings(self):
        """Сохранение настроек"""
        self.settings.beginGroup("Transformer")
        self.settings.setValue("tr_from_db", self.ui.radioButton_tr_from_db.isChecked())
        self.settings.setValue('tr_manufacturer', self.ui.comboBox_tr_manufacturer.currentText())
        self.settings.setValue('tr_model', self.ui.comboBox_tr_model.currentText())
        self.settings.setValue('U_sr_VN', self.ui.comboBox_U_sr_VN.currentText())
        self.settings.setValue('U_sr_NN', self.ui.comboBox_U_sr_NN.currentText())
        self.settings.setValue('tr_connection_windings', self.ui.comboBox_tr_connection_windings.currentText())
        self.settings.setValue('tr_full_rated_capacity', self.ui.comboBox_tr_full_rated_capacity.currentText())
        self.settings.setValue('tr_short_circuit_loss', self.ui.comboBox_tr_short_circuit_loss.currentText())
        self.settings.setValue('tr_impedance_voltage', self.ui.comboBox_tr_impedance_voltage.currentText())
        self.settings.setValue('Rt', self.ui.lineEdit_Rt.text())
        self.settings.setValue('Xt', self.ui.lineEdit_Xt.text())
        self.settings.setValue('R0t', self.ui.lineEdit_R0t.text())
        self.settings.setValue('X0t', self.ui.lineEdit_X0t.text())
        self.settings.endGroup()

        self.settings.beginGroup("3ph_short_circuit_current_HV")
        self.settings.setValue('Sk_IkVN_Xs_Iotklnom', self.ui.lineEdit_Sk_IkVN_Xs.text())
        self.settings.setValue('xc_mode', self.ui.comboBox_Sk_IkVN_Xs.currentIndex())
        self.settings.endGroup()

        self.settings.beginGroup("Line")
        self.settings.setValue('Rsh', self.ui.lineEdit_Rsh.text())
        self.settings.setValue('Xsh', self.ui.lineEdit_Xsh.text())
        self.settings.setValue('R_1kb', self.ui.lineEdit_R_1kb.text())
        self.settings.setValue('X_1kb', self.ui.lineEdit_X_1kb.text())
        self.settings.setValue('Rvl', self.ui.lineEdit_Rvl.text())
        self.settings.setValue('Xvl', self.ui.lineEdit_Xvl.text())
        self.settings.setValue('R0sh', self.ui.lineEdit_R0sh.text())
        self.settings.setValue('X0sh', self.ui.lineEdit_X0sh.text())
        self.settings.setValue('R_0kb', self.ui.lineEdit_R_0kb.text())
        self.settings.setValue('X_0kb', self.ui.lineEdit_X_0kb.text())
        self.settings.setValue('R0vl', self.ui.lineEdit_R0vl.text())
        self.settings.setValue('X0vl', self.ui.lineEdit_X0vl.text())
        self.settings.endGroup()

        self.settings.beginGroup("Other_circuit_elements")
        self.settings.setValue('Other_circuit_elements_tab', self.ui.tabWidget_2.currentIndex())
        self.settings.setValue('Rpr', self.ui.lineEdit_Rpr.text())
        self.settings.setValue('Xpr', self.ui.lineEdit_Xpr.text())
        self.settings.setValue('Rr', self.ui.lineEdit_Rr.text())
        self.settings.setValue('Xr', self.ui.lineEdit_Xr.text())
        self.settings.setValue('Rk', self.ui.lineEdit_Rk.text())
        self.settings.setValue('Rkv', self.ui.lineEdit_Rkv.text())
        self.settings.setValue('Xkv', self.ui.lineEdit_Xkv.text())
        self.settings.setValue('Rta', self.ui.lineEdit_Rta.text())
        self.settings.setValue('Xta', self.ui.lineEdit_Xta.text())
        self.settings.setValue('Rd', self.ui.lineEdit_Rd.text())
        self.settings.endGroup()

    # @property
    def my_function(self):
        """
        Основная функция программы
        """

        # Очистить данные предыдущих вычислений
        self.clear_results()

        # Считывание данных системы
        try:
            # Параметры системы
            U_sr_VN = 1
            U_sr_NN = 0
            switch = "Xs"
            Sk_IkVN_Xs_Iotklnom = 0
            U_sr_VN = float(self.ui.comboBox_U_sr_VN.currentText())
            U_sr_NN = float(self.ui.comboBox_U_sr_NN.currentText())
            Sk_IkVN_Xs_Iotklnom = float(self.ui.lineEdit_Sk_IkVN_Xs.text())
        except ValueError:
            msg = "Исходные данные системы введены не корректно. Сопротивление системы в расчётах не учитывается."
            self.statusBar().showMessage(msg)
        else:
            def switch_Xc(xc_mode):
                """
                Определение положения переключателя для определения
                тока КЗ на выводах ВН
                """
                return {
                    0: "Sk",
                    1: "IkVN",
                    2: "Xs"
                }.get(xc_mode, "Iotklnom")

            switch = switch_Xc(self.ui.comboBox_Sk_IkVN_Xs.currentIndex())

        # Считывание данных трансформатора
        try:
            # Параметры трансформатора
            Rt = 0
            Xt = 0
            R0t = 0
            X0t = 0
            Rt = float(self.ui.lineEdit_Rt.text())
            Xt = float(self.ui.lineEdit_Xt.text())
            R0t = float(self.ui.lineEdit_R0t.text())
            X0t = float(self.ui.lineEdit_X0t.text())
        except ValueError:
            msg = ("Исходные данные трансформатора введены не корректно. " +
                   "Сопротивление трансформатора в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Считывание данных шинопровода
        try:
            Rsh = 0
            Xsh = 0
            R0sh = 0
            X0sh = 0
            Rsh = float(self.ui.lineEdit_Rsh.text())
            Xsh = float(self.ui.lineEdit_Xsh.text())
            R0sh = float(self.ui.lineEdit_R0sh.text())
            X0sh = float(self.ui.lineEdit_X0sh.text())
        except ValueError:
            msg = ("Исходные данные шинопровода введены не корректно. " +
                   "Сопротивление шинопровода в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Считывание данных кабельной линии
        try:
            R_1kb = 0
            X_1kb = 0
            R_0kb = 0
            X_0kb = 0
            R_1kb = float(self.ui.lineEdit_R_1kb.text())
            X_1kb = float(self.ui.lineEdit_X_1kb.text())
            R_0kb = float(self.ui.lineEdit_R_0kb.text())
            X_0kb = float(self.ui.lineEdit_X_0kb.text())
        except ValueError:
            msg = ("Исходные данные кабельной линии введены не корректно. " +
                   "Сопротивление кабельной линии в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Считывание данных воздушной линии
        try:
            Rvl = 0
            Xvl = 0
            R0vl = 0
            X0vl = 0
            Rvl = float(self.ui.lineEdit_Rvl.text())
            Xvl = float(self.ui.lineEdit_Xvl.text())
            R0vl = float(self.ui.lineEdit_R0vl.text())
            X0vl = float(self.ui.lineEdit_X0vl.text())
        except ValueError:
            msg = ("Исходные данные воздушной линии введены не корректно. " +
                   "Сопротивление воздушной линии в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Выбрана вкладка "Кратко"
        # Считывание данных остальных элементов цепи
        try:
            Rpr = 0
            Xpr = 0
            if self.ui.tabWidget_2.currentIndex() == 0:
                Rpr = float(self.ui.lineEdit_Rpr.text())
                Xpr = float(self.ui.lineEdit_Xpr.text())
        except ValueError:
            msg = ("Исходные данные остальных элементов цепи введены не корректно. " +
                   "Сопротивление остальных элементов цепи в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Выбрана вкладка "Подробно"
        # Считывание данных реактора
        try:
            Rr = 0
            Xr = 0
            if self.ui.tabWidget_2.currentIndex() == 1:
                Rr = float(self.ui.lineEdit_Rr.text())
                Xr = float(self.ui.lineEdit_Xr.text())
        except ValueError:
            msg = ("Исходные данные реактора введены не корректно. " +
                   "Сопротивление реактора в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Считывание данных контактов и контактных соединений
        try:
            Rk = 0
            if self.ui.tabWidget_2.currentIndex() == 1:
                Rk = float(self.ui.lineEdit_Rk.text())
        except ValueError:
            msg = ("Исходные данные контактов введены не корректно. " +
                   "Сопротивление контактов в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Считывание данных катушек автоматических выключателей
        try:
            Rkv = 0
            Xkv = 0
            if self.ui.tabWidget_2.currentIndex() == 1:
                Rkv = float(self.ui.lineEdit_Rkv.text())
                Xkv = float(self.ui.lineEdit_Xkv.text())
        except ValueError:
            msg = ("Исходные данные катушек автоматических выключателей введены не корректно. " +
                   "Сопротивление катушек автоматических выключателей в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Считывание данных первичных обмоток трансформаторов тока
        try:
            Rta = 0
            Xta = 0
            if self.ui.tabWidget_2.currentIndex() == 1:
                Rta = float(self.ui.lineEdit_Rta.text())
                Xta = float(self.ui.lineEdit_Xta.text())
        except ValueError:
            msg = ("Исходные данные первичных обмоток трансформаторов тока введены не корректно. " +
                   "Сопротивление первичных обмоток трансформаторов тока в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        # Считывание данных дуги
        try:
            Rd = 0
            if self.ui.tabWidget_2.currentIndex() == 1:
                Rd = float(self.ui.lineEdit_Rd.text())
        except ValueError:
            msg = ("Исходные данные дуги введены не корректно. " +
                   "Сопротивление дуги в расчётах не учитывается.")
            self.statusBar().showMessage(msg)

        try:
            pass
        except ValueError:
            self.statusBar().showMessage('Введите исходные данные.')
        # except Exception:
        # Заглушка для всех ошибок
        #            print('Это что ещё такое?')
        else:
            [self.Ip0_3ph_max, self.Ip0_3ph_min, self.i_a0_3ph_max, self.i_a0_3ph_min, self.i_ud_3ph_max,
             self.i_ud_3ph_min,
             self.Ip0_1ph_max, self.Ip0_1ph_min, self.i_a0_1ph_max, self.i_a0_1ph_min, self.i_ud_1ph_max,
             self.i_ud_1ph_min,
             self.Ip0_2ph_max, self.Ip0_2ph_min, self.i_a0_2ph_max, self.i_a0_2ph_min, self.i_ud_2ph_max,
             self.i_ud_2ph_min] = sccc.calc_short_current(
                switch, Sk_IkVN_Xs_Iotklnom, U_sr_NN, U_sr_VN,  # Система
                Rt, Xt, R0t, X0t,  # Трансформатор
                Rpr, Xpr,  # Прочие элементы цепи, заданные одним значением
                # Pr_nom_delta=0, Ir_nom=0, f=0, L=0, M=0,  # Реактор
                Rr, Xr,  # Реактор
                Rta, Xta,  # Трансформаторы тока
                Rkv, Xkv,  # Катушки автоматических выключателей
                Rsh, Xsh, R0sh, X0sh,  # Шинопровод
                Rk,  # Контакты
                R_1kb, X_1kb, R_0kb, X_0kb,  # Кабельная линия
                Rvl, Xvl, R0vl, X0vl,  # Воздушная линия
                Rd)  # Дуга
            if math.isinf(self.Ip0_3ph_max) or math.isinf(self.Ip0_1ph_max) or math.isinf(self.Ip0_2ph_max):
                msg = "Исходные данные заданые не корректно. Сопротивление расчётного участка сети равно нулю."
                self.statusBar().showMessage(msg)
            else:
                self.ui.label_Ip0max_3ph.setText("{:.2f}".format(self.Ip0_3ph_max))
                self.ui.label_Ipomin_3ph.setText("{:.2f}".format(self.Ip0_3ph_min))
                self.ui.label_i_ud_max_3ph.setText("{:.2f}".format(self.i_ud_3ph_max))
                self.ui.label_i_ud_min_3ph.setText("{:.2f}".format(self.i_ud_3ph_min))
                self.ui.label_i_ao_max_3ph.setText("{:.2f}".format(self.i_a0_3ph_max))
                self.ui.label_i_ao_min_3ph.setText("{:.2f}".format(self.i_a0_3ph_min))
                self.ui.label_Ip0max_1ph.setText("{:.2f}".format(self.Ip0_1ph_max))
                self.ui.label_Ipomin_1ph.setText("{:.2f}".format(self.Ip0_1ph_min))
                self.ui.label_i_ud_max_1ph.setText("{:.2f}".format(self.i_ud_1ph_max))
                self.ui.label_i_ud_min_1ph.setText("{:.2f}".format(self.i_ud_1ph_min))
                self.ui.label_i_ao_max_1ph.setText("{:.2f}".format(self.i_a0_1ph_max))
                self.ui.label_i_ao_min_1ph.setText("{:.2f}".format(self.i_a0_1ph_min))
                self.ui.label_Ip0max_2ph.setText("{:.2f}".format(self.Ip0_2ph_max))
                self.ui.label_Ipomin_2ph.setText("{:.2f}".format(self.Ip0_2ph_min))
                self.ui.label_i_ud_max_2ph.setText("{:.2f}".format(self.i_ud_2ph_max))
                self.ui.label_i_ud_min_2ph.setText("{:.2f}".format(self.i_ud_2ph_min))
                self.ui.label_i_ao_max_2ph.setText("{:.2f}".format(self.i_a0_2ph_max))
                self.ui.label_i_ao_min_2ph.setText("{:.2f}".format(self.i_a0_2ph_min))
                msg = "Расчёт закончен успешно."
                self.statusBar().showMessage(msg)
        finally:
            # Выбирается вкладка "Результаты"
            self.ui.tabWidget.setCurrentWidget(self.ui.tab_results)

    def clear_results(self):
        """Очистка результатов вычислений"""
        # pass
        self.ui.label_Ip0max_3ph.setText("-")
        self.ui.label_i_ao_max_3ph.setText("-")
        self.ui.label_i_ud_max_3ph.setText("-")
        self.ui.label_Ipomin_3ph.setText("-")
        self.ui.label_i_ao_min_3ph.setText("-")
        self.ui.label_i_ud_min_3ph.setText("-")

    def save_report_odt(self):
        """Сохранение отчёта в файл ODT"""
        # Ip0_3ph_max_exp = str(self.Ip0_3ph_max)
        # if not self.Ip0_3ph_max:
        #     print("Нет данных для отчёта")
        # else:
        context = dict()
        context["Ip0_1ph_max_exp"] = "{:.2f}".format(self.Ip0_1ph_max)
        context["Ip0_1ph_min_exp"] = "{:.2f}".format(self.Ip0_1ph_min)
        context["i_ud_1ph_max_exp"] = "{:.2f}".format(self.i_ud_1ph_max)
        context["i_ud_1ph_min_exp"] = "{:.2f}".format(self.i_ud_1ph_min)
        context["i_a0_1ph_max_exp"] = "{:.2f}".format(self.i_a0_1ph_max)
        context["i_a0_1ph_min_exp"] = "{:.2f}".format(self.i_a0_1ph_min)
        context["Ip0_2ph_max_exp"] = "{:.2f}".format(self.Ip0_2ph_max)
        context["Ip0_2ph_min_exp"] = "{:.2f}".format(self.Ip0_2ph_min)
        context["i_ud_2ph_max_exp"] = "{:.2f}".format(self.i_ud_2ph_max)
        context["i_ud_2ph_min_exp"] = "{:.2f}".format(self.i_ud_2ph_min)
        context["i_a0_2ph_max_exp"] = "{:.2f}".format(self.i_a0_2ph_max)
        context["i_a0_2ph_min_exp"] = "{:.2f}".format(self.i_a0_2ph_min)
        context["Ip0_3ph_max_exp"] = "{:.2f}".format(self.Ip0_3ph_max)
        context["Ip0_3ph_min_exp"] = "{:.2f}".format(self.Ip0_3ph_min)
        context["i_ud_3ph_max_exp"] = "{:.2f}".format(self.i_ud_3ph_max)
        context["i_ud_3ph_min_exp"] = "{:.2f}".format(self.i_ud_3ph_min)
        context["i_a0_3ph_max_exp"] = "{:.2f}".format(self.i_a0_3ph_max)
        context["i_a0_3ph_min_exp"] = "{:.2f}".format(self.i_a0_3ph_min)
        # context = dict(Ip0_3ph_max_exp=str(self.Ip0_3ph_max))
        # beingPaidForIt = True
        # renderer = Renderer('./template/А4_Приложение_test.odt', globals(), './template/result.odt')
        renderer = Renderer("./template/А4_Приложение_test.odt", context, "./template/result.odt",
                            overwriteExisting=True)
        renderer.run()

    @QtCore.pyqtSlot()
    def open_file_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Считать данные из файла", "",
                                                  "INI Files (*.ini)", options=options)
        if fileName:
            self.settings = QtCore.QSettings(fileName, QtCore.QSettings.IniFormat)
            self.settings.setIniCodec("utf-8")
            self.read_settings()

    @QtCore.pyqtSlot()
    def save_file_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить файл с текущими данными", "",
                                                  "INI Files (*.ini)", options=options)
        if fileName:
            self.settings = QtCore.QSettings(fileName, QtCore.QSettings.IniFormat)
            self.settings.setIniCodec("utf-8")
            self.save_settings()

    @QtCore.pyqtSlot()
    def show_about_window(self):
        """Отображение окна сведений о программе"""
        return QMessageBox.about(self, "О программе", "Описание программы")

    @QtCore.pyqtSlot()
    def show_aboutqt_window(self):
        """Отображение окна сведений о библиотеке Qt"""
        return QMessageBox.aboutQt(self)

    @QtCore.pyqtSlot()
    def show_db_window(self):
        self.dbwindow = dbwindow.DBWindow()
        self.dbwindow.show()

    @QtCore.pyqtSlot()
    def add_cable_from_db(self):
        """Добавление кабеля из базы данных"""
        self.addcabledialog = addcabledialog.AddCableDialog()
        result = self.addcabledialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            linetype = self.addcabledialog.ui.comboBox_linetype.currentText()
            material_of_cable = self.addcabledialog.ui.comboBox_material_of_cable_core.currentText()
            size_of_cable_phase = self.addcabledialog.ui.comboBox_size_of_cable_phase.currentText()
            size_of_cable_neutral = self.addcabledialog.ui.comboBox_size_of_cable_neutral.currentText()
            resistance = dboperations.find_resistance(linetype, material_of_cable, size_of_cable_phase,
                                                      size_of_cable_neutral)
            linelength = self.addcabledialog.ui.doubleSpinBox_linelength.value()
            parallel_fider = self.addcabledialog.ui.spinBox_parallel_fider.value()
            r1 = float(resistance[0]) * linelength / parallel_fider
            x1 = float(resistance[1]) * linelength / parallel_fider
            r0 = float(resistance[2]) * linelength / parallel_fider
            x0 = float(resistance[3]) * linelength / parallel_fider
            self.ui.lineEdit_R_1kb.setText("{:.2f}".format(r1))
            self.ui.lineEdit_X_1kb.setText("{:.2f}".format(x1))
            self.ui.lineEdit_R_0kb.setText("{:.2f}".format(r0))
            self.ui.lineEdit_X_0kb.setText("{:.2f}".format(x0))

    @QtCore.pyqtSlot()
    def add_aerial_line_from_db(self):
        """Добавление кабеля из базы данных"""
        self.addcabledialog = addcabledialog.AddCableDialog()
        result = self.addcabledialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            linetype = self.addcabledialog.ui.comboBox_linetype.currentText()
            material_of_cable = self.addcabledialog.ui.comboBox_material_of_cable_core.currentText()
            size_of_cable_phase = self.addcabledialog.ui.comboBox_size_of_cable_phase.currentText()
            size_of_cable_neutral = self.addcabledialog.ui.comboBox_size_of_cable_neutral.currentText()
            resistance = dboperations.find_resistance(linetype, material_of_cable, size_of_cable_phase,
                                                      size_of_cable_neutral)
            linelength = self.addcabledialog.ui.doubleSpinBox_linelength.value()
            parallel_fider = self.addcabledialog.ui.spinBox_parallel_fider.value()
            r1 = float(resistance[0]) * linelength / parallel_fider
            x1 = float(resistance[1]) * linelength / parallel_fider
            r0 = float(resistance[2]) * linelength / parallel_fider
            x0 = float(resistance[3]) * linelength / parallel_fider
            self.ui.lineEdit_Rvl.setText("{:.2f}".format(r1))
            self.ui.lineEdit_Xvl.setText("{:.2f}".format(x1))
            self.ui.lineEdit_R0vl.setText("{:.2f}".format(r0))
            self.ui.lineEdit_X0vl.setText("{:.2f}".format(x0))

    @QtCore.pyqtSlot()
    def add_busway_from_db(self):
        """Добавление кабеля из базы данных"""
        self.addcabledialog = addcabledialog.AddCableDialog()
        result = self.addcabledialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            linetype = self.addcabledialog.ui.comboBox_linetype.currentText()
            material_of_cable = self.addcabledialog.ui.comboBox_material_of_cable_core.currentText()
            size_of_cable_phase = self.addcabledialog.ui.comboBox_size_of_cable_phase.currentText()
            size_of_cable_neutral = self.addcabledialog.ui.comboBox_size_of_cable_neutral.currentText()
            resistance = dboperations.find_resistance(linetype, material_of_cable, size_of_cable_phase,
                                                      size_of_cable_neutral)
            linelength = self.addcabledialog.ui.doubleSpinBox_linelength.value()
            parallel_fider = self.addcabledialog.ui.spinBox_parallel_fider.value()
            r1 = float(resistance[0]) * linelength / parallel_fider
            x1 = float(resistance[1]) * linelength / parallel_fider
            r0 = float(resistance[2]) * linelength / parallel_fider
            x0 = float(resistance[3]) * linelength / parallel_fider
            self.ui.lineEdit_Rsh.setText("{:.2f}".format(r1))
            self.ui.lineEdit_Xsh.setText("{:.2f}".format(x1))
            self.ui.lineEdit_R0sh.setText("{:.2f}".format(r0))
            self.ui.lineEdit_X0sh.setText("{:.2f}".format(x0))


class QRV(QtGui.QRegExpValidator):
    def __init__(self, reg_exp_str):
        super().__init__(QtCore.QRegExp(reg_exp_str))

    def validate(self, text, pos):
        res, s, i = super().validate(text, pos)
        s = self.fixup(text) if res != QtGui.QValidator.Acceptable else s
        return res, s, i

    @classmethod
    def fixup(cls, s):
        s = s.replace(',', '.') if ',' in s else s
        return s


if __name__ == "__main__":
    # QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv)  # pylint: disable=invalid-name
    myapp = MyWin("last_values.ini")
    myapp.show()
    sys.exit(app.exec_())

# TODO Добавить данные в БД
# TODO Данные по умолчанию для сопротивлений прочих элементов цепи
# TODO Расчёт сопротивления дуги
# TODO Учёт влияния нагрева провода
# TODO Учёт комплексной нагрузки
# TODO Возможность задания нескольких участков кабеля
# TODO Возможность проверки нескольких точек КЗ
# TODO Проверка аппарата защиты

# TODO Добавление в базу данных (копирование, проверка на заполнение всех полей, проверка на наличие аналогичных
# записей)
# TODO QSystemTrayIcon (свернуть приложение в трей)
