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

    # add range to filter
    def AddNodesToNetwork (self):
        nodes = self.FilterNodes(2000)
        self.graph.add_nodes_from(nodes)

    def addEdgesToNetwork(self):
        return

    def FilterNodes (self, yearfilter):
        conferenceNodes = []
        for key, value in self.conferenceDetails.items():
            if int(value['year']) == yearfilter:
                conferenceNodes.append(key)
        print(conferenceNodes)
        return conferenceNodes
