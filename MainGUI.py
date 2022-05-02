from PyQt5 import QtWidgets, uic
import sys

from DirectedGUI import DGUi

class MUi(QtWidgets.QMainWindow):
    def openDirectedWindow(self):
        self.ui = DGUi()
        

    def __init__(self):
        super(MUi,self).__init__()
        uic.loadUi('MainWindow.ui',self)

        self.setFixedSize(804, 156)

        self.dirPushBut.clicked.connect(self.openDirectedWindow)

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MUi()
    app.exec_()