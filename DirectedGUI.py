from PyQt5 import QtWidgets, uic, QtWebEngineWidgets, QtCore, QtGui
import sys
import os.path

from graph import GraphPlot

class DGUi(QtWidgets.QMainWindow):

    Nodes = []
    Edges = []

    def reGraph(self):
        GraphPlot.plotDir(self.Nodes,self.Edges)
        self.graphBrowser.load(QtCore.QUrl.fromLocalFile(os.path.abspath("graph.html")))
    
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
                if nH < 0:
                    raise Exception("No Negative Numbers")
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
                self.reGraph()
                if len(self.Nodes) >= 2:
                    ngg = list(filter(lambda node: node['goal'], self.Nodes))
                    if (len(ngg) != len(self.Nodes)) and (len(ngg) >= 1):
                        self.searchBtn.setDisabled(False)

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
                if eC < 0:
                    raise Exception("No Negative Numbers")
                self.Edges.append({"from":self.fromEdAddCom.currentText(),"to":self.toEdAddCom.currentText(),"cost":eC})
                self.delEdCom.addItem(self.fromEdAddCom.currentText() + " > " + self.toEdAddCom.currentText() + " : " + str(eC))
                self.fromEdAddCom.setCurrentIndex(-1)
                self.toEdAddCom.setCurrentIndex(-1)
                self.edPathCTxt.setText("")
                self.reGraph()

        except:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('error.png'))
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please check that Edge Path Cost is valid')
            msg.setWindowTitle("Error")
            msg.exec_()

    def delNode(self):
        if self.delNodeCom.currentIndex() != -1:
            nL = list(filter(lambda node: node['name'] != self.delNodeCom.currentText(), self.Nodes))
            nE = list(filter(lambda edge: edge['from'] != self.delNodeCom.currentText(), self.Edges))
            nE = list(filter(lambda edge: edge['to'] != self.delNodeCom.currentText(), nE))
            self.Edges = nE
            self.Nodes = nL
            fC = [self.fromEdAddCom.itemText(i) for i in range(self.fromEdAddCom.count())]
            for i in range(0,len(fC)):
                if fC[i] == self.delNodeCom.currentText():
                    self.fromEdAddCom.removeItem(i)
            tC = [self.toEdAddCom.itemText(i) for i in range(self.toEdAddCom.count())]
            for i in range(0,len(tC)):
                if tC[i] == self.delNodeCom.currentText():
                    self.toEdAddCom.removeItem(i)
            sC = [self.startNodeCom.itemText(i) for i in range(self.startNodeCom.count())]
            for i in range(0,len(sC)):
                if sC[i] == self.delNodeCom.currentText():
                    self.startNodeCom.removeItem(i)
            self.delNodeCom.removeItem(self.delNodeCom.currentIndex())
            self.reGraph()
            if len(self.Nodes) < 2:    
                self.searchBtn.setDisabled(True)
            else:
                ngg = list(filter(lambda node: node['goal'], self.Nodes))
                if (len(ngg) == len(self.Nodes)) or (len(ngg) < 1):
                    self.searchBtn.setDisabled(True)
            dEc = [self.delEdCom.itemText(i) for i in range(self.delEdCom.count())]
            for i in range(0,len(dEc)):
                Ef, Et = dEc[i].split('>')
                Ef.strip()
                Et, Ec = Et.split(':')
                Et.strip()
                Ec = float(Ec)
                if next((edge for edge in self.Edges if ((edge['from'] == Ef) or (edge['to'] == Et))), None)  == None:
                    self.delEdCom.removeItem(i)            
            self.delNodeCom.setCurrentIndex(-1)   

    def delEdge(self):
        if self.delEdCom.currentIndex() != -1:
            Ef, Et = self.delEdCom.currentText().split('>')
            Ef.strip()
            Et, Ec = Et.split(':')
            Et.strip()
            Ec = float(Ec)
            nE = list(filter(lambda edge: (edge['from'] != Ef) and (edge['to'] != Et) and (edge['cost'] != Ec), self.Edges))
            self.Edges = nE
            self.delEdCom.removeItem(self.delEdCom.currentIndex())
            self.reGraph()
            self.delEdCom.setCurrentIndex(-1)
            
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
        self.graphBrowser.setObjectName("graphBrowser")
        self.reGraph()

        self.treeBrowser = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.treeBrowser.setGeometry(QtCore.QRect(560, 220, 551, 601))
        self.treeBrowser.setObjectName("treeBrowser")

        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setGeometry(QtCore.QRect(1050, 230, 51, 31))
        self.nextBtn.setObjectName("nextBtn")
        self.nextBtn.setText("Next")
        self.nextBtn.setDisabled(True) 

        self.fromEdAddCom.lineEdit().setPlaceholderText("From")
        self.toEdAddCom.lineEdit().setPlaceholderText("To")
        self.delEdCom.lineEdit().setPlaceholderText("Pick an Edge to Delete")
        self.delNodeCom.lineEdit().setPlaceholderText("Pick a Node to Delete")
        self.startNodeCom.lineEdit().setPlaceholderText("Pick a Starting Node")
        self.searchAlgoCom.lineEdit().setPlaceholderText("Pick a Searching Algorithm")
        self.searchBtn.setDisabled(True)

        self.searchAlgoCom.addItem("Breadth First Search")
        self.searchAlgoCom.addItem("Depth First Search")
        self.searchAlgoCom.addItem("Iterative Deepening Search")
        self.searchAlgoCom.addItem("Uniform Cost Search")
        self.searchAlgoCom.addItem("Greedy Search")
        self.searchAlgoCom.addItem("A* Search")

        self.adNodeBtn.clicked.connect(self.addNode)
        self.adEdgeBtn.clicked.connect(self.addEdge)
        self.checkBox.clicked.connect(self.checkBoxClick)
        self.delNodeBtn.clicked.connect(self.delNode)
        self.delEdgeBtn.clicked.connect(self.delEdge)

        self.show()

        ##This is for finding functions using auto complete as they cannot be found with the item loaded in the .ui
        #self.x = QtWidgets.QComboBox(self.centralwidget)
        #self.x.setCurrentIndex(-1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DGUi()
    app.exec_()