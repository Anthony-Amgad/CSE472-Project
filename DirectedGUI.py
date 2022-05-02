from PyQt5 import QtWidgets, uic, QtWebEngineWidgets, QtCore, QtGui
import sys
import os.path

class DGUi(QtWidgets.QMainWindow):

    Nodes = []
    Edges = []
    
    def addNode(self):
        try:
            if next((x for x in self.Nodes if x["name"] == self.nodeNameTxt.text()), None)  != None:
                msg = QtWidgets.QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('error.png'))
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Please Enter Unique Node Name')
                msg.setWindowTitle("Error")
                msg.exec_()
            elif self.nodeNameTxt.text() == "":
                msg = QtWidgets.QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('error.png'))
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Please Make sure the Node Name is entered')
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                nH = self.nodeHuerTxt.text()
                if nH == "":
                    nH = 0
                else:
                    nH = float(nH)
                nG = self.checkBox.isChecked()
                nN = self.nodeNameTxt.text()
                self.Nodes.append({"name":nN, "heur":nH, "goal":nG})
                self.fromEdAddCom.addItem(nN)
                self.toEdAddCom.addItem(nN)
                self.delNodeCom.addItem(nN)
                self.nodeNameTxt.setText("")
                self.nodeHuerTxt.setDisabled(False)
                self.nodeHuerTxt.setText("")
                self.checkBox.setCheckState(False)
                if not nG:
                    self.startNodeCom.addItem(nN)

        except:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('error.png'))
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please check that Node Heuristic is valid')
            msg.setWindowTitle("Error")
            msg.exec_()

    
    def addEdge(self):
        try:
            if (self.fromEdAddCom.currentIndex() == -1) or (self.toEdAddCom.currentIndex() == -1):
                msg = QtWidgets.QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('error.png'))
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Please Make sure both a from and to Node are selected')
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                eC = self.edPathCTxt.text()
                if eC == "":
                    eC = 0
                else:
                    eC = float(eC)
                self.Edges.append({"from":self.fromEdAddCom.currentIndex(),"to":self.toEdAddCom.currentIndex(),"cost":eC})
                self.delEdCom.addItem(self.fromEdAddCom.currentText() + " > " + self.toEdAddCom.currentText() + " : " + str(eC))
                self.fromEdAddCom.setCurrentIndex(-1)
                self.toEdAddCom.setCurrentIndex(-1)
                self.edPathCTxt.setText("")

        except:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('error.png'))
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please check that Edge Path Cost is valid')
            msg.setWindowTitle("Error")
            msg.exec_()

    def checkBoxClick(self):
        if self.checkBox.isChecked():
            self.nodeHuerTxt.setDisabled(True)
            self.nodeHuerTxt.setText("0")
        else:
            self.nodeHuerTxt.setDisabled(False)
            self.nodeHuerTxt.setText("")

    
    def __init__(self):
        super(DGUi,self).__init__()
        uic.loadUi('DirectedWindow.ui',self)

        self.setWindowIcon(QtGui.QIcon('img.png'))


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

        self.adNodeBtn.clicked.connect(self.addNode)
        self.adEdgeBtn.clicked.connect(self.addEdge)
        self.checkBox.clicked.connect(self.checkBoxClick)

        self.show()

        ##This is for finding functions using auto complete as they cannot be found with the item loaded in the .ui
        self.x = QtWidgets.QComboBox(self.centralwidget)
        self.x.setCurrentIndex(-1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DGUi()
    app.exec_()