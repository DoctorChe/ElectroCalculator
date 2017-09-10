#!/usr/bin/python3
# -*- coding: utf-8 -*-
"Программа для вычисления токов короткого замыкания"

import sys
# Импортируем наш интерфейс из файла
from ui_mainwindow import Ui_MainWindow
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication#, QWidget
from PyQt5.QtCore import QSettings
# from PyQt5.QtWidgets import QAction
# from PyQt5 import QtCore, QtGui
# from PyQt5 import uic
# from PyQt5.uic import loadUi
# from short_circuit_current_calculation import calc_Ip0_3ph
import short_circuit_current_calculation as sccc


#class MyWin(QtWidgets.QMainWindow):
class MyWin(QMainWindow):
    """
    Основной класс программы
    """
    def __init__(self, iniFile, parent=None):
#        QtWidgets.QWidget.__init__(self, parent)
#        QWidget.__init__(self, parent)
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = QSettings(iniFile, QSettings.IniFormat)
        self.settings.setIniCodec("utf-8")
        # Чтение настроек
        self.read_settings()

#        uic.loadUi("MainWindow.ui", self)
#        widget = loadUi('demo.ui')
#        self.ui = uic.loadUi('Ui_MainWindow.ui')

        # Событие - запуск вычисления
        self.ui.action_Calculate.triggered.connect(self.my_function)

        # Событие - выход из программы
        self.ui.action_Exit.triggered.connect(self.close)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.my_function)
#        self.ui.pushButton.clicked.connect(self.ui.action_Exit)
#        self.ui.pushButton.addAction(self.ui.action_Exit)

#        self.ui.lineEdit.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))


    def closeEvent(self, e): # pylint: disable=invalid-name
        """
        Обработка события закрытия программы
        """
        # Write data to config file
        self.save_settings()
        e.accept()

    def read_settings(self):
        """
        Чтение настроек
        """
#        self.inputs = {}
#        self.params = []
#        ini.beginGroup("Common")
#        wt = ini.value('Title','')
#        if wt != '': self.setWindowTitle(wt)
#        ini.endGroup()
        self.settings.beginGroup("Transformer")
        self.lineEdit_U_sr_VN_State = self.settings.value("U_sr_VN", 10)
        self.ui.lineEdit_U_sr_VN.setText(str(self.lineEdit_U_sr_VN_State))
        self.lineEdit_U_sr_NN_State = self.settings.value("U_sr_NN", 400)
        self.ui.lineEdit_U_sr_NN.setText(str(self.lineEdit_U_sr_NN_State))
        self.settings.endGroup()
        self.settings.beginGroup("3ph_short_circuit_current_HV")
        self.lineEdit_Sk_IkVN_Xs_State = self.settings.value("Sk_IkVN_Xs_Iotklnom", 0)
        self.ui.lineEdit_Sk_IkVN_Xs.setText(str(self.lineEdit_Sk_IkVN_Xs_State))
        self.comboBox_Sk_IkVN_Xs_State = self.settings.value("xc_mode", 2)
        self.ui.comboBox_Sk_IkVN_Xs.setCurrentIndex(int(self.comboBox_Sk_IkVN_Xs_State))
        self.settings.endGroup()
#        chBoxState = settings.value('chBoxState', QtCore.Qt.Checked)
#        self.chB.setCheckState(int(chBoxState))
 

    def save_settings(self):
        """
        Сохранение настроек
        """
        self.settings.beginGroup("Transformer")
        self.settings.setValue('U_sr_VN', self.ui.lineEdit_U_sr_VN.text())
        self.settings.setValue('U_sr_NN', self.ui.lineEdit_U_sr_NN.text())
        self.settings.endGroup()
        self.settings.beginGroup("3ph_short_circuit_current_HV")
        self.settings.setValue('Sk_IkVN_Xs_Iotklnom', self.ui.lineEdit_Sk_IkVN_Xs.text())
        self.settings.setValue('xc_mode', self.ui.comboBox_Sk_IkVN_Xs.currentIndex())
        self.settings.endGroup()
#        self.layoutSettings.sync()
    

#    def loadIni(self, iniFile):
#        ini = QSettings(iniFile, QSettings.IniFormat)
#        ini.setIniCodec("utf-8")

    def my_function(self):
        """
        Основная функция программы
        """
        self.ui.lineEdit_Ip0_3ph.clear()
        try:
            U_sr_VN = float(self.ui.lineEdit_U_sr_VN.text()) # pylint: disable=invalid-name
            U_sr_NN = float(self.ui.lineEdit_U_sr_NN.text()) # pylint: disable=invalid-name
#            R_1sum = float(self.ui.lineEdit_R_1sum.text())
#            X_1sum = float(self.ui.lineEdit_X_1sum.text())

            Sk_IkVN_Xs_Iotklnom = float(self.ui.lineEdit_Sk_IkVN_Xs.text()) # pylint: disable=invalid-name
        except ValueError:
            self.statusBar().showMessage('Введите исходные данные.')
#        except Exception:
            # Заглушка для всех ошибок
#            print('Это что ещё такое?')
        else:
            def switch_Xc(xc_mode): # pylint: disable=invalid-name
                """
                Определение положения переключателя для определения
                тока КЗ на выводах ВН
                """
                return{
                    0: "Sk",
                    1: "IkVN",
                    2: "Xs"
                    }.get(xc_mode, "Iotklnom")
            switch = switch_Xc(self.ui.comboBox_Sk_IkVN_Xs.currentIndex())
#            Ip0_3ph = sccc.calc_Ip0_3ph(R_1sum, X_1sum, U_sr_NN)
            Ip0_3ph = sccc.calc_short_current( # pylint: disable=invalid-name
                switch, Sk_IkVN_Xs_Iotklnom, U_sr_NN, U_sr_VN,
                Pk_nom=0, U_NN_nom=0.4, St_nom=0, u_k=0,
                Pr_nom_delta=0, Ir_nom=0, f=0, L=0, M=0,
                RtA=0, XtA=0,
                Rkv=0, Xkv=0,
                Rsh=0, Xsh=0,
                Rk=0,
                R_1kb=0, X_1kb=0,
                Rvl=0, Xvl=0,
                Rd=0)
            self.ui.lineEdit_Ip0_3ph.setText(str(round(Ip0_3ph, 1)))
        finally:
            # Выбирается вкладка "Результаты"
            self.ui.tabWidget.setCurrentIndex(4)

#    def clear(self):
#        """
#        Очистка результатов вычислений
#        """
#        self.ui.lineEdit_Ip0_3ph.clear()

if __name__ == "__main__":
    QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv) # pylint: disable=invalid-name
    myapp = MyWin("last_values.ini") # pylint: disable=invalid-name
    myapp.show()
    sys.exit(app.exec_())
