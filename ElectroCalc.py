import sys
# Импортируем наш интерфейс из файла
from ui_mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
#from PyQt5 import QtCore, QtGui
#from PyQt5 import uic
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
        self.ui.pushButton.clicked.connect(self.ui.action_Exit)
#        self.ui.pushButton.addAction(self.ui.action_Exit)

#        self.ui.lineEdit.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку
    def my_function(self):
        try:
            a = float(self.ui.lineEdit_A.text())
            b = float(self.ui.lineEdit_B.text())
        except ValueError:
            self.statusBar().showMessage('Введите число.')
        except Exception:
            # Заглушка для всех ошибок
            print('Это что ещё такое?')
        else:
            c = short_current_calc(a, b)
            self.ui.lineEdit_C.setText(str(c))
        finally:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
