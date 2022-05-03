from tkinter.tix import Tree
from pyvis.network import Network

class TreePlot:

    def plot(treeNodes, expanded, found):

        G = Network(height='100%', width='100%', directed=True ,layout=Tree)

        for n in treeNodes:
            
            G.add_node(n["name"]+":"+str(n["Gs"]), n["name"] + " ( G:" + str(n["Gs"]) + " H:" + str(n["Hs"]) + " )", shape="ellipse")
            if n["parent"] != None:
                G.add_edge(n["parent"], n["name"]+":"+str(n["Gs"]))

        for n in expanded:
            G.get_node(n)["color"] = 'lime'
            

        if found:
            G.get_node(expanded[-1])["color"] = 'yellow'

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