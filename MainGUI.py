from PyQt5 import QtWidgets, uic, QtGui
import sys

from DirectedGUI import DGUi
from UndirectedGUI import UGUi

class MUi(QtWidgets.QMainWindow):
    def openDirectedWindow(self):
        self.ui = DGUi()

    def openUnDirectedWindow(self):
        self.ui = UGUi()
        
    def __init__(self):
        super(MUi,self).__init__()
        uic.loadUi('res/MainWindow.ui',self)

        self.setFixedSize(804, 156)

        self.setWindowIcon(QtGui.QIcon('res/img.png'))

        self.dirPushBut.clicked.connect(self.openDirectedWindow)
        self.undirPushBut.clicked.connect(self.openUnDirectedWindow)

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MUi()
    app.exec_()