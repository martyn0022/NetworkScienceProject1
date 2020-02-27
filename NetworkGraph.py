# requires installation
import networkx as nx
import matplotlib.pyplot as plt

conferenceDetails = {}
# conferences are the nodes

graph = nx.Graph()


def initialize (conf):
    print("initializing networkgraph")
    conferenceDetails = conf
    nodes = FilterNodes(2015)
    graph.add_nodes_from(nodes)
    nx.draw(graph)
    plt.savefig("test.png")


def FilterNodes (year):
    conferenceNodes = []
    for conf, attr in conferenceDetails.item():
        if attr["year"] == str(year):
            conferenceNodes.append(conf)
    return conferenceNodes
