# requires installation
import networkx as nx
import matplotlib.pyplot as plt


class Network:
    def __init__ (self, conf):
        self.conferenceDetails = conf
        # conferences are the nodes
        self.graph = nx.Graph()

    def DrawGraph (self):
        self.AddNodesToNetwork()
        nx.draw(self.graph)
        plt.savefig("test.png")

    # add range to filter
    def AddNodesToNetwork (self):
        nodes = self.FilterNodes(2000)
        edges = self.addEdgesToNetwork(nodes)
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

    def addEdgesToNetwork (self, nodes):
        edges = []
        for key1 in nodes:
            for key2 in nodes:
                weight = 0
                if key1 != key2:
                    for author1 in self.conferenceDetails[key1]['authors']:
                        if author1 in self.conferenceDetails[key2]['authors']:
                            weight += 1
                    if weight > 0:
                        edges.append((key1, key2, {'weight': weight}))

        '''
        for key1, conference1 in self.conferenceDetails.items():
            for key2, conference2 in self.conferenceDetails.items():
                weight = 0
                if key1 != key2:
                    for author1 in conference1['authors']:
                        if author1 in conference2['authors']:
                            weight += 1
                    if weight > 0:
                        edges.append((key1, key2, {'weight': weight}))
        '''
        return edges

    def FilterNodes (self, yearfilter):
        conferenceNodes = []
        for key, value in self.conferenceDetails.items():
            if int(value['year']) == yearfilter:
                conferenceNodes.append(key)
        print(conferenceNodes)
        return conferenceNodes
