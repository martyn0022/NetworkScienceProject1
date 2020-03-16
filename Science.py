import collections
from operator import itemgetter
import json

import networkx as nx
import matplotlib.pyplot as plt


# Get data from JSON
def ParseJSONtoDict (filename):
    # Read JSON data into the datastore variable
    if filename:
        with open(filename, 'r') as f:
            datastore = json.load(f)
    return datastore


# Store data into JSON
def SaveNodesEdgesinJSON (nodes, edges, fileName):
    with open('json/'+fileName+'Nodes.json', 'w') as json_file:
        json.dump(nodes, json_file)

    with open('json/'+fileName+'Edges.json', 'w') as json_file:
        json.dump(edges, json_file)


class Networks:
    def __init__ (self):
        self.conferenceDiGraph = nx.DiGraph()
        self.authorGraph = nx.Graph()

        self.CreateConferenceNetwork()
        self.CreateAuthorNetwork()


    def CreateConferenceNetwork (self):
        nodes = ParseJSONtoDict('json/conferenceNodes.json')
        edges = ParseJSONtoDict('json/conferenceEdges.json')
        self.conferenceDiGraph.add_nodes_from(nodes)
        self.conferenceDiGraph.add_weighted_edges_from(edges)


    def CreateAuthorNetwork (self):
        nodes = ParseJSONtoDict('json/authorNodes.json')
        edges = ParseJSONtoDict('json/authorEdges.json')
        self.authorGraph.add_nodes_from(nodes)
        self.authorGraph.add_edges_from(edges)


    def GetConferenceGraph(self):
        return self.conferenceDiGraph


    def GetAuthorGraph(self):
        return self.authorGraph

    def GetNumberOfAuthors(self):
        return len(self.authorGraph.nodes)

    def GetNumberOfConferences(self):
        return len(self.conferenceDiGraph.nodes)


def FilterConferenceNodes(conferenceGraph, startyear=1950, endyear=2017, minTier=3, minSize=0):
    filteredNodes = []

    for node in conferenceGraph.nodes.data():
        if node[1]['year'] in list(range(startyear, endyear)):
            if node[1]['tier'] <= minTier:
                if node[1]['size'] >= minSize:
                    filteredNodes.append(node[0])

    conferenceSubGraph = conferenceGraph.subgraph(filteredNodes).copy()

    return conferenceSubGraph


# chris
def FilterAuthorNodes(authorGraph, startyear=1950, endyear=2017, min=1, max=4000, minSuccess = 0):
    filteredNodes = []

    for node in authorGraph.nodes.data():
        if node[1]['start'] >= startyear and node[1]['end'] <= endyear:
            if node[1]['success'] >= minSuccess:
                filteredNodes.append(node[0])

    authorSubGraph = authorGraph.subgraph(filteredNodes).copy()

    return authorSubGraph


def GetDegreeDistribution(graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    degList, degCountList = zip(*degreeCount.items())

    # print(degList, degCountList)

    return degList, degCountList


# Chris
def GetBetweenness(graph):
    #access specific node by using betweennessList[node]
    betweennessList = nx.betweenness_centrality(graph)

    for key, value in betweennessList.items():
        if value > 0:
            print(key, value)


# Chris
def GetEigenVector(graph):
    #access specific node by using EigenMatrix[node]
    eigenMatrix = nx.eigenvector_centrality(graph)
    print(eigenMatrix)


# Chris
def GetCloseness(graph):
    #acess specific node by using closeness[node]
    closenessList = nx.closeness_centrality(graph)
    print(closenessList)


def DrawGraph(graph):
    nodessize = []
    edgecolors = []
    nodescolor = []

    edgeslist = graph.edges.data()

    for node in graph.nodes.data():
        nodessize.append(node[1]['size'])
        if node[1]['tier'] == 1:
            nodescolor.append([1,0,0])
        elif node[1]['tier'] == 2:
            nodescolor.append([1,0.2,0.2])
        elif node[1]['tier'] == 3:
            nodescolor.append([1,0.4,0.4])

    maxSize = max(nodessize)
    minSize = min(nodessize)
    maxNodeSize = 5000
    for size in nodessize:
        size = (size - minSize) / (maxSize -minSize) * maxNodeSize + 1000

    edgemax = max(edgeslist, key=lambda x: x[2]['weight'])[2]['weight']
    edgemin = min(edgeslist, key=lambda x: x[2]['weight'])[2]['weight']
    M = graph.number_of_edges()
    edgealphas = []
    for edge in edgeslist:
        weight = edge[2]['weight']
        color = (weight - edgemin) / (edgemax - edgemin)
        edgecolors.append(color)
        edgealphas.append(color)

    # plt.figure(figsize=(20,20))
    pos=nx.spring_layout(graph, k=5)

    nx.draw_networkx_nodes(
        graph,
        pos=pos,
        node_color=nodescolor,
        node_size=nodessize
    )

    edges = nx.draw_networkx_edges(
        graph,
        pos=pos,
        arrowstyle="->",
        arrowsize=5,
        edge_color=edgecolors,
        edge_cmap=plt.cm.Greys,
        width=1,
    )

    nx.draw_networkx_labels(
        graph, pos=pos, font_size=6,
        font_color='k', font_family='sans-serif',
        font_weight='normal', alpha=None,
        bbox=None, ax=None
    )

    # set alpha value for each edge
    for i in range(M):
        edges[i].set_alpha(edgealphas[i])

    plt.savefig("conferenceNW.png")


def CreateAuthorDistribution(authorGraph):
    maxDegree = max(authorGraph.degree, key=lambda x: x[1])[1]
    minDegree = min(authorGraph.degree, key=lambda x: x[1])[1]

    publication_seq = []
    for node in authorGraph.nodes.data():
        publication_seq.append(node[1]['size'])
    publication_seq = sorted(publication_seq, reverse=True)
    publicationCount = collections.Counter(publication_seq)

    N = len(authorGraph.nodes)
    pk = []
    count=0
    for publNum,cnt in publicationCount.items():
        pk.append(publNum/N)
        if publNum > 100:
            count += cnt
    print(count)
    pk = sorted(pk, reverse=True)

    publ, cnt = zip(*publicationCount.items())
    print(publ)

    ax = plt.gca()
    ax.scatter(publ, cnt, c="r")
    plt.title("Author Publications Distribution")
    plt.ylabel("Count")
    plt.xlabel("Publications")
    ax.set(xscale="log")
    ax.set(yscale="log")
    plt.savefig("AuthorPublicationsDistribution.png")
    # graph too large to be drawn, but algorithms based on degree etc, can be done

    plt.close
