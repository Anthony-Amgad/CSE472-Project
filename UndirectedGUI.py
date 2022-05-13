from PyQt5 import QtWidgets, uic, QtWebEngineWidgets, QtCore, QtGui
import sys
import os.path

from graph import GraphPlot
from tree import TreePlot


class UGUi(QtWidgets.QMainWindow):

    Nodes = []
    Edges = []
    visited = []
    fringe = []
    expanded = []
    treeNodes = []
    temtree = []
    AdjLi = {}
    choice = None
    curDLS = 1

    def reGraph(self):
        self.AdjLi = GraphPlot.plotUnDir(self.Nodes,self.Edges)
        self.graphBrowser.load(QtCore.QUrl.fromLocalFile(os.path.abspath("rec/graph.html")))

    def reTree(self, found):
        TreePlot.plot(self.treeNodes, self.expanded, found)
        self.treeBrowser.load(QtCore.QUrl.fromLocalFile(os.path.abspath("rec/tree.html")))
    
    def addNode(self):
        try:
            if next((x for x in self.Nodes if x["name"] == self.nodeNameTxt.text()), None)  != None:
                msg = QtWidgets.QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('rec/error.png'))
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Please Enter Unique Node Name')
                msg.setWindowTitle("Error")
                msg.exec_()
            elif self.nodeNameTxt.text() == "":
                msg = QtWidgets.QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('rec/error.png'))
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
            msg.setWindowIcon(QtGui.QIcon('rec/error.png'))
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please check that Node Heuristic is valid')
            msg.setWindowTitle("Error")
            msg.exec_()

    
    def addEdge(self):
        try:
            if (self.fromEdAddCom.currentIndex() == -1) or (self.toEdAddCom.currentIndex() == -1):
                msg = QtWidgets.QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('rec/error.png'))
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
                self.delEdCom.addItem(self.fromEdAddCom.currentText() + " - " + self.toEdAddCom.currentText() + " : " + str(eC))
                self.fromEdAddCom.setCurrentIndex(-1)
                self.toEdAddCom.setCurrentIndex(-1)
                self.edPathCTxt.setText("")
                self.reGraph()

        except:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('rec/error.png'))
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
                Ef, Et = dEc[i].split('-')
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


    def onClickSearch(self):
        if (self.startNodeCom.currentIndex() != -1) and (self.searchAlgoCom.currentIndex() != -1):
            temheur = next(x for x in self.Nodes if x["name"] == self.startNodeCom.currentText())["heur"]
            self.fringe.append(self.startNodeCom.currentText() + ":0:" + str(temheur) + ":1")
            self.treeNodes.append({"name" : self.startNodeCom.currentText(), "parent" : None, "Gs" : 0, "Hs" : temheur, "goal":next(x for x in self.Nodes if x["name"] == self.startNodeCom.currentText())["goal"], "hi":1})
            self.choice = self.searchAlgoCom.currentIndex()
            self.curDLS = 1
            self.temtree = []
            self.inSearch(True)
            self.reTree(False)
                
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('rec/error.png'))
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Make sure you chose a starting node and an algorithm')
            msg.setWindowTitle("Error")
            msg.exec_()

    def onClickNext(self):
        match self.choice:
            case 0: #BFS
                if len(self.fringe) == 0:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowIcon(QtGui.QIcon('rec/warning.png'))
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setText("A goal node cannot be reached")
                    msg.setInformativeText('This starting node cannot reach a goal node')
                    msg.setWindowTitle("Warning")
                    msg.exec_()
                    self.inSearch(False)
                    self.fringe.clear()
                    self.expanded.clear()
                    self.treeNodes.clear()
                else:
                    parent = self.fringe.pop(0)
                    self.expanded.append(parent)
                    pn, pg, ph, pt = parent.split(":")
                    if next(x for x in self.Nodes if x["name"] == pn)["goal"]:
                        self.reTree(True)
                        path = []
                        pp = parent
                        while pp != None:
                            ppn, ppg, pph, ppt = pp.split(":")
                            path.append(ppn)
                            pp = next(x for x in self.treeNodes if ((x["name"] == ppn) and (x["Gs"] == float(ppg))))["parent"]
                        st = ""
                        path.reverse()
                        for p in path:
                            st = st + p + " -> "
                        st = st[:-3]
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowIcon(QtGui.QIcon('rec/info.png'))
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText("Node Path Discovered: ")
                        msg.setInformativeText(st)
                        msg.setWindowTitle("Path")
                        msg.exec_()
                        self.inSearch(False)
                        self.fringe.clear()
                        self.expanded.clear()
                        self.treeNodes.clear()
                    else:
                        for child in self.AdjLi[pn]:
                            eL = list(filter(lambda edge: ((edge['from'] == pn) and (edge['to'] == child)) or ((edge['to'] == pn) and (edge['from'] == child)), self.Edges))
                            gS = min(eL, key=lambda x:x['cost'])['cost'] + float(pg)
                            hI = int(pt) + 1
                            hS = next(x for x in self.Nodes if x["name"] == child)['heur']
                            if not any((ele.find(child + ":") != -1) and (ele.find(":" + str(hS) + ":") != -1) for ele in self.expanded):
                                self.fringe.append(child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                self.treeNodes.append({"name":child,"parent":parent,"Gs":gS,"Hs":hS, "goal":next(x for x in self.Nodes if x["name"] == child)['goal'] ,"hi":hI})
                        self.reTree(False)
            case 1: #DFS
                    if len(self.fringe) == 0:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowIcon(QtGui.QIcon('rec/warning.png'))
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setText("A goal node cannot be reached")
                        msg.setInformativeText('This starting node cannot reach a goal node')
                        msg.setWindowTitle("Warning")
                        msg.exec_()
                        self.inSearch(False)
                        self.fringe.clear()
                        self.expanded.clear()
                        self.treeNodes.clear()
                    else:
                        parent = self.fringe.pop(-1)
                        self.expanded.append(parent)
                        pn, pg, ph, pt = parent.split(":")
                        if next(x for x in self.Nodes if x["name"] == pn)["goal"]:
                            self.reTree(True)
                            path = []
                            pp = parent
                            while pp != None:
                                ppn, ppg, pph, ppt = pp.split(":")
                                path.append(ppn)
                                pp = next(x for x in self.treeNodes if ((x["name"] == ppn) and (x["Gs"] == float(ppg))))["parent"]
                            st = ""
                            path.reverse()
                            for p in path:
                                st = st + p + " -> "
                            st = st[:-3]
                            msg = QtWidgets.QMessageBox()
                            msg.setWindowIcon(QtGui.QIcon('rec/info.png'))
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setText("Node Path Discovered: ")
                            msg.setInformativeText(st)
                            msg.setWindowTitle("Path")
                            msg.exec_()
                            self.inSearch(False)
                            self.fringe.clear()
                            self.expanded.clear()
                            self.treeNodes.clear()
                        else:
                            for child in self.AdjLi[pn]:
                                eL = list(filter(lambda edge: ((edge['from'] == pn) and (edge['to'] == child)) or ((edge['to'] == pn) and (edge['from'] == child)), self.Edges))
                                gS = min(eL, key=lambda x:x['cost'])['cost'] + float(pg)
                                hI = int(pt) + 1
                                hS = next(x for x in self.Nodes if x["name"] == child)['heur']
                                if not any((ele.find(child + ":") != -1) and (ele.find(":" + str(hS) + ":") != -1) for ele in self.expanded):
                                    self.fringe.append(child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                    self.treeNodes.append({"name":child,"parent":parent,"Gs":gS,"Hs":hS, "goal":next(x for x in self.Nodes if x["name"] == child)['goal'], "hi":hI})
                            self.reTree(False)
            case 2: #IDDFS
                    if (len(self.fringe) == 0) and (self.temtree == self.treeNodes):
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowIcon(QtGui.QIcon('rec/warning.png'))
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setText("A goal node cannot be reached")
                        msg.setInformativeText('This starting node cannot reach a goal node')
                        msg.setWindowTitle("Warning")
                        msg.exec_()
                        self.inSearch(False)
                        self.fringe.clear()
                        self.expanded.clear()
                        self.treeNodes.clear()
                    elif len(self.fringe) == 0:
                        self.temtree = self.treeNodes.copy()
                        self.expanded.clear()
                        tem = self.treeNodes[0]
                        self.treeNodes.clear()
                        self.treeNodes.append(tem)
                        self.fringe.append(tem["name"] + ":0:" + str(tem["Hs"]) + ":1")
                        self.reTree(False)
                        self.curDLS += 1
                    else:
                        parent = self.fringe.pop(-1)
                        self.expanded.append(parent)
                        pn, pg, ph, pt = parent.split(":")
                        if next(x for x in self.Nodes if x["name"] == pn)["goal"]:
                            self.reTree(True)
                            path = []
                            pp = parent
                            while pp != None:
                                ppn, ppg, pph, ppt = pp.split(":")
                                path.append(ppn)
                                pp = next(x for x in self.treeNodes if ((x["name"] == ppn) and (x["Gs"] == float(ppg))))["parent"]
                            st = ""
                            path.reverse()
                            for p in path:
                                st = st + p + " -> "
                            st = st[:-3]
                            msg = QtWidgets.QMessageBox()
                            msg.setWindowIcon(QtGui.QIcon('rec/info.png'))
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setText("Node Path Discovered: ")
                            msg.setInformativeText(st)
                            msg.setWindowTitle("Path")
                            msg.exec_()
                            self.inSearch(False)
                            self.fringe.clear()
                            self.expanded.clear()
                            self.treeNodes.clear()
                        else:
                            for child in self.AdjLi[pn]:
                                eL = list(filter(lambda edge: ((edge['from'] == pn) and (edge['to'] == child)) or ((edge['to'] == pn) and (edge['from'] == child)), self.Edges))
                                gS = min(eL, key=lambda x:x['cost'])['cost'] + float(pg)
                                hI = int(pt) + 1
                                hS = next(x for x in self.Nodes if x["name"] == child)['heur']
                                if not any((ele.find(child + ":") != -1) and (ele.find(":" + str(hS) + ":") != -1) for ele in self.expanded):
                                    if hI <= self.curDLS:
                                        self.fringe.append(child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                        self.treeNodes.append({"name":child,"parent":parent,"Gs":gS,"Hs":hS, "goal":next(x for x in self.Nodes if x["name"] == child)['goal'], "hi":hI})
                            self.reTree(False)
            case 3: #UCS
                    if len(self.fringe) == 0:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowIcon(QtGui.QIcon('rec/warning.png'))
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setText("A goal node cannot be reached")
                        msg.setInformativeText('This starting node cannot reach a goal node')
                        msg.setWindowTitle("Warning")
                        msg.exec_()
                        self.inSearch(False)
                        self.fringe.clear()
                        self.expanded.clear()
                        self.treeNodes.clear()
                    else:
                        parent = self.fringe.pop(0)
                        self.expanded.append(parent)
                        pn, pg, ph, pt = parent.split(":")
                        if next(x for x in self.Nodes if x["name"] == pn)["goal"]:
                            self.reTree(True)
                            path = []
                            pp = parent
                            while pp != None:
                                ppn, ppg, pph, ppt = pp.split(":")
                                path.append(ppn)
                                pp = next(x for x in self.treeNodes if ((x["name"] == ppn) and (x["Gs"] == float(ppg))))["parent"]
                            st = ""
                            path.reverse()
                            for p in path:
                                st = st + p + " -> "
                            st = st[:-3]
                            msg = QtWidgets.QMessageBox()
                            msg.setWindowIcon(QtGui.QIcon('rec/info.png'))
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setText("Node Path Discovered: ")
                            msg.setInformativeText(st)
                            msg.setWindowTitle("Path")
                            msg.exec_()
                            self.inSearch(False)
                            self.fringe.clear()
                            self.expanded.clear()
                            self.treeNodes.clear()
                        else:
                            for child in self.AdjLi[pn]:
                                eL = list(filter(lambda edge: ((edge['from'] == pn) and (edge['to'] == child)) or ((edge['to'] == pn) and (edge['from'] == child)), self.Edges))
                                gS = min(eL, key=lambda x:x['cost'])['cost'] + float(pg)
                                hI = int(pt) + 1
                                hS = next(x for x in self.Nodes if x["name"] == child)['heur']
                                if not any((ele.find(child + ":") != -1) and (ele.find(":" + str(hS) + ":") != -1) for ele in self.expanded):
                                    ff = True
                                    for i in range(0,len(self.fringe)):
                                        iin,iig,iih,iit = self.fringe[i].split(":")
                                        if float(iig) > gS:
                                            self.fringe.insert(i,child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                            ff = False
                                            break
                                    if ff :
                                        self.fringe.append(child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                    self.treeNodes.append({"name":child,"parent":parent,"Gs":gS,"Hs":hS, "goal":next(x for x in self.Nodes if x["name"] == child)['goal'] , "hi" : hI})
                            self.reTree(False)
            case 4: #GS
                    if len(self.fringe) == 0:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowIcon(QtGui.QIcon('rec/warning.png'))
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setText("A goal node cannot be reached")
                        msg.setInformativeText('This starting node cannot reach a goal node')
                        msg.setWindowTitle("Warning")
                        msg.exec_()
                        self.inSearch(False)
                        self.fringe.clear()
                        self.expanded.clear()
                        self.treeNodes.clear()
                    else:
                        parent = self.fringe.pop(0)
                        self.expanded.append(parent)
                        pn, pg, ph, pt = parent.split(":")
                        if next(x for x in self.Nodes if x["name"] == pn)["goal"]:
                            self.reTree(True)
                            path = []
                            pp = parent
                            while pp != None:
                                ppn, ppg, pph, ppt = pp.split(":")
                                path.append(ppn)
                                pp = next(x for x in self.treeNodes if ((x["name"] == ppn) and (x["Gs"] == float(ppg))))["parent"]
                            st = ""
                            path.reverse()
                            for p in path:
                                st = st + p + " -> "
                            st = st[:-3]
                            msg = QtWidgets.QMessageBox()
                            msg.setWindowIcon(QtGui.QIcon('rec/info.png'))
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setText("Node Path Discovered: ")
                            msg.setInformativeText(st)
                            msg.setWindowTitle("Path")
                            msg.exec_()
                            self.inSearch(False)
                            self.fringe.clear()
                            self.expanded.clear()
                            self.treeNodes.clear()
                        else:
                            for child in self.AdjLi[pn]:
                                eL = list(filter(lambda edge: ((edge['from'] == pn) and (edge['to'] == child)) or ((edge['to'] == pn) and (edge['from'] == child)), self.Edges))
                                gS = min(eL, key=lambda x:x['cost'])['cost'] + float(pg)
                                hI = int(pt) + 1
                                hS = next(x for x in self.Nodes if x["name"] == child)['heur']
                                if not any((ele.find(child + ":") != -1) and (ele.find(":" + str(hS) + ":") != -1) for ele in self.expanded):
                                    ff = True
                                    for i in range(0,len(self.fringe)):
                                        iin,iig,iih,iit = self.fringe[i].split(":")
                                        if float(iih) > hS:
                                            self.fringe.insert(i,child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                            ff = False
                                            break
                                    if ff :
                                        self.fringe.append(child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                    self.treeNodes.append({"name":child,"parent":parent,"Gs":gS,"Hs":hS, "goal":next(x for x in self.Nodes if x["name"] == child)['goal'], "hi":hI})
                            self.reTree(False)
            case 5: #A*S
                    if len(self.fringe) == 0:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowIcon(QtGui.QIcon('rec/warning.png'))
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setText("A goal node cannot be reached")
                        msg.setInformativeText('This starting node cannot reach a goal node')
                        msg.setWindowTitle("Warning")
                        msg.exec_()
                        self.inSearch(False)
                        self.fringe.clear()
                        self.expanded.clear()
                        self.treeNodes.clear()
                    else:
                        parent = self.fringe.pop(0)
                        self.expanded.append(parent)
                        pn, pg, ph, pt = parent.split(":")
                        if next(x for x in self.Nodes if x["name"] == pn)["goal"]:
                            self.reTree(True)
                            path = []
                            pp = parent
                            while pp != None:
                                ppn, ppg, pph, ppt = pp.split(":")
                                path.append(ppn)
                                pp = next(x for x in self.treeNodes if ((x["name"] == ppn) and (x["Gs"] == float(ppg))))["parent"]
                            st = ""
                            path.reverse()
                            for p in path:
                                st = st + p + " -> "
                            st = st[:-3]
                            msg = QtWidgets.QMessageBox()
                            msg.setWindowIcon(QtGui.QIcon('rec/info.png'))
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setText("Node Path Discovered: ")
                            msg.setInformativeText(st)
                            msg.setWindowTitle("Path")
                            msg.exec_()
                            self.inSearch(False)
                            self.fringe.clear()
                            self.expanded.clear()
                            self.treeNodes.clear()
                        else:
                            for child in self.AdjLi[pn]:
                                eL = list(filter(lambda edge: ((edge['from'] == pn) and (edge['to'] == child)) or ((edge['to'] == pn) and (edge['from'] == child)), self.Edges))
                                gS = min(eL, key=lambda x:x['cost'])['cost'] + float(pg)
                                hI = int(pt) + 1
                                hS = next(x for x in self.Nodes if x["name"] == child)['heur']
                                if not any((ele.find(child + ":") != -1) and (ele.find(":" + str(hS) + ":") != -1) for ele in self.expanded):
                                    ff = True
                                    for i in range(0,len(self.fringe)):
                                        iin,iig,iih,iit = self.fringe[i].split(":")
                                        if (float(iig)+float(iih)) > (gS+hS):
                                            self.fringe.insert(i,child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                            ff = False
                                            break
                                    if ff :
                                        self.fringe.append(child + ":" + str(gS) + ":" + str(hS) + ":" + str(hI))
                                    self.treeNodes.append({"name":child,"parent":parent,"Gs":gS,"Hs":hS, "goal":next(x for x in self.Nodes if x["name"] == child)['goal'], "hi":hI})
                            self.reTree(False) 

                       
    def inSearch(self, bool):
        self.nextBtn.setDisabled(not bool)
        self.adNodeBtn.setDisabled(bool)
        self.adEdgeBtn.setDisabled(bool)
        self.delNodeBtn.setDisabled(bool)
        self.delEdgeBtn.setDisabled(bool)
        self.searchBtn.setDisabled(bool)

    
    def __init__(self):
        super(UGUi,self).__init__()
        uic.loadUi('rec/GraphingWindow.ui',self)

        self.Nodes = []
        self.Edges = []
        self.visited = []
        self.fringe = []
        self.expanded = []
        self.treeNodes = []
        self.temtree = []
        self.AdjLi = {}
        self.choice = None
        self.maxDep = None
        self.curDLS = 1

        self.setWindowIcon(QtGui.QIcon('rec/img.png'))
        self.setWindowTitle("Undirected Graph")

        self.setFixedSize(1112, 858)
        
        self.graphBrowser = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.graphBrowser.setGeometry(QtCore.QRect(0, 220, 551, 601))
        self.graphBrowser.setObjectName("graphBrowser")
        self.reGraph()

        self.treeBrowser = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.treeBrowser.setGeometry(QtCore.QRect(560, 220, 551, 601))
        self.treeBrowser.setObjectName("treeBrowser")
        self.reTree(False)

        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setGeometry(QtCore.QRect(1050, 230, 51, 31))
        self.nextBtn.setObjectName("nextBtn")
        self.nextBtn.setText("Next")
        self.nextBtn.setDisabled(True) 

        self.fromEdAddCom.lineEdit().setPlaceholderText("First Node")
        self.toEdAddCom.lineEdit().setPlaceholderText("Second Node")
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
        self.searchBtn.clicked.connect(self.onClickSearch)
        self.nextBtn.clicked.connect(self.onClickNext)

        self.show()

        ##This is for finding functions using auto complete as they cannot be found with the item loaded in the .ui
        #self.x = QtWidgets.QComboBox(self.centralwidget)
        #self.x.setCurrentIndex(-1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UGUi()
    app.exec_()