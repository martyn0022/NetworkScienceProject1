# requires installation
import networkx as nx
import matplotlib.pyplot as plt


class Network:
    def __init__(self, conf):
        print("initializing networkgraph")
        self.conferenceDetails = conf
        # conferences are the nodes
        self.graph = nx.Graph()

    def DrawGraph(self):
        self.AddNodesToNetwork()
        nx.draw(self.graph)
        plt.savefig("test.png")

    def AddNodesToNetwork (self):
        nodes = self.FilterNodes(2015)
        self.graph.add_nodes_from(nodes)

    def FilterNodes (self, year):
        conferenceNodes = []
        print(len(self.conferenceDetails[str(year)]))
        for conf in self.conferenceDetails[str(year)].items():
            conferenceNodes.append(conf[1]["name"])
        print(conferenceNodes)
        return conferenceNodes
