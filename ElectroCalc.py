import sys
# Импортируем наш интерфейс из файла
from MainWindow import *
from PyQt5 import QtCore, QtGui, QtWidgets


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.my_function)

        self.ui.lineEdit.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку
    def my_function(self):
        # self.ui.lineEdit_3.setText(str(float(self.ui.lineEdit.text()) + float(self.ui.lineEdit_2.text())))
        a = float(self.ui.lineEdit.text())
        # self.ui.lineEdit_3.setText(self.ui.lineEdit.text() * 5)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
