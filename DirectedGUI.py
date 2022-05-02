from PyQt5 import QtWidgets, uic, QtWebEngineWidgets, QtCore
import sys
import os.path

class DGUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(DGUi,self).__init__()
        uic.loadUi('DirectedWindow.ui',self)

        self.setFixedSize(1112, 858)
        
        self.graphBrowser = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.graphBrowser.setGeometry(QtCore.QRect(0, 220, 551, 601))
        self.graphBrowser.setObjectName("graphBrowseri")
        self.graphBrowser.load(QtCore.QUrl.fromLocalFile(os.path.abspath("test.html")))

        self.treeBrowser = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.treeBrowser.setGeometry(QtCore.QRect(560, 220, 551, 601))
        self.treeBrowser.setObjectName("treeBrowser")
        self.treeBrowser.load(QtCore.QUrl.fromLocalFile(os.path.abspath("test.html")))

        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setGeometry(QtCore.QRect(1050, 230, 51, 31))
        self.nextBtn.setObjectName("nextBtn")
        self.nextBtn.setText("Next")    

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