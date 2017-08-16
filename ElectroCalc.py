import sys
# Импортируем наш интерфейс из файла
from ui_mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QAction
# from PyQt5 import QtCore, QtGui
# from PyQt5 import uic
# from PyQt5.uic import loadUi
# from short_circuit_current_calculation import calc_Ip0_3ph
import short_circuit_current_calculation as sccc


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку
    def my_function(self):
        self.ui.lineEdit_Ip0_3ph.clear()
        try:
            U_sr_VN = float(self.ui.lineEdit_U_sr_VN.text())
            U_sr_NN = float(self.ui.lineEdit_U_sr_NN.text())
#            R_1sum = float(self.ui.lineEdit_R_1sum.text())
#            X_1sum = float(self.ui.lineEdit_X_1sum.text())

            Sk_IkVN_Xs_Iotklnom = float(self.ui.lineEdit_Sk_IkVN_Xs.text())
        except ValueError:
            self.statusBar().showMessage('Введите исходные данные.')
#        except Exception:
            # Заглушка для всех ошибок
#            print('Это что ещё такое?')
        else:
            def switch_Xc(x):
                return{
                        0: "Sk",
                        1: "IkVN",
                        2: "Xs"
                        }.get(x, "Iotklnom")
            switch = switch_Xc(self.ui.comboBox_Sk_IkVN_Xs.currentIndex())
#            Ip0_3ph = sccc.calc_Ip0_3ph(R_1sum, X_1sum, U_sr_NN)
            Ip0_3ph = sccc.calc_short_current(
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
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
