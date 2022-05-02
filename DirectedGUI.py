from PyQt5 import QtWidgets, uic
import sys

class DGUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(DGUi,self).__init__()
        uic.loadUi('DirectedWindow.ui',self)

        self.fromEdAddCom.lineEdit().setPlaceholderText("From")
        self.toEdAddCom.lineEdit().setPlaceholderText("To")
        self.delEdCom.lineEdit().setPlaceholderText("Pick an Edge to Delete")
        self.delNodeCom.lineEdit().setPlaceholderText("Pick a Node to Delete")
        self.startNodeCom.lineEdit().setPlaceholderText("Pick a Starting Node")
        self.searchAlgoCom.lineEdit().setPlaceholderText("Pick a Searching Algorithm")

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DGUi()
    app.exec_()