
from pyvis.network import Network

class Plot:

    def plotDir(Nodes,Edges):
        G = Network(height='100%', width='100%', directed=True)

        G.set_options("""var options = {
                  "edges": {
                    "smooth": {
                        "enabled" : true
                    },
                    "color": {
                        "inherit" : false
                    }
                  },
                  "interaction": {
                    "hover": true,
                    "keyboard": {
                      "enabled": true
                    },
                    "multiselect": true,
                    "navigationButtons": true
                  }
                }
        """)

        for n in Nodes:
            if n["goal"]:
                G.add_node(n["name"], n["name"] + " : " + str(n["heur"]), shape="ellipse", color = "yellow")
            else:
                G.add_node(n["name"], n["name"] + " : " + str(n["heur"]), shape="ellipse")

        for e in Edges:
            G.add_edge(e["from"], e["to"], label = e["cost"])

        G.save_graph("Dir.html")


