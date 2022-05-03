from tkinter.tix import Tree
from pyvis.network import Network

class TreePlot:

    def plot(treeNodes, expanded, found):

        G = Network(height='100%', width='100%', directed=True ,layout=Tree)

        for n in treeNodes:
            
            G.add_node(n["name"], n["name"] + " ( H:" + str(n["Hs"]) + " G:" + str(n["Gs"]) + " )", shape="ellipse")
            if n["parent"] != None:
                pn,pg = n["parent"].split(":")
                G.add_edge(pn, n["name"])

        for n in expanded:
            nn,ng = n.split(":")
            G.get_node(nn)["color"] = 'lime'

        if found:
            G.get_node(expanded[-1].split(":")[0])["color"] = 'yellow'

        G.save_graph("tree.html")


#G = Network(layout=Tree)

#G.add_node("aa","aa")
#G.add_node("ab","ab")
#G.add_node("ac","ac")
#G.add_node("ad","ad")
#G.add_edge("aa","ab")
#G.add_edge("aa","ac")
#G.add_edge("ab","ad")


#G.show("tree.html")