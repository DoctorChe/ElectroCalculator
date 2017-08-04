import sys
# Импортируем наш интерфейс из файла
from ui_mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QAction
# from PyQt5 import QtCore, QtGui
# from PyQt5 import uic
# from PyQt5.uic import loadUi
from short_circuit_current_calculation import *


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
#        self.ui.pushButton.clicked.connect(self.ui.action_Exit)
#        self.ui.pushButton.addAction(self.ui.action_Exit)

#        self.ui.lineEdit.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку
    def my_function(self):
        try:
            U_sr_NN = float(self.ui.lineEdit_U_sr_NN.text())
            R_1sum = float(self.ui.lineEdit_R_1sum.text())
            X_1sum = float(self.ui.lineEdit_X_1sum.text())
        except ValueError:
            self.statusBar().showMessage('Введите число.')
        except Exception:
            # Заглушка для всех ошибок
            print('Это что ещё такое?')
        else:
            Ip0_3ph = calc_Ip0_3ph(R_1sum, X_1sum, U_sr_NN)
            self.ui.lineEdit_Ip0_3ph.setText(str(Ip0_3ph))
#            self.ui.tab_5.
        finally:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
