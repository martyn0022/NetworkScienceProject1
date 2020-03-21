import collections
from operator import itemgetter
import json

import networkx as nx
import numpy as np
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
        self.conferenceDiGraph2 = nx.DiGraph()
        self.authorGraph = nx.Graph()

        self.CreateConferenceNetwork()
        self.CreateAuthorNetwork()
        self.NewConferenceGraph()


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

    def GetConferenceGraph2(self):
        return self.conferenceDiGraph2

    def GetAuthorGraph(self):
        return self.authorGraph

    def GetNumberOfAuthors(self):
        return len(self.authorGraph.nodes)

    def GetNumberOfConferences(self):
        return len(self.conferenceDiGraph.nodes)

    def CreateGraphForGUI(self, network='author', measure='degree'):
        if network == 'author':
            x,y = GetDegreeDistribution(self.authorGraph)

        return x,y

    def NewConferenceGraph(self):
        conferenceGraph = self.conferenceDiGraph
        nodes = []
        for node in conferenceGraph.nodes.data():
            conftype = node[0][0:-4]
            if conftype == 'vldb':
                conftype = 'pvldb'
            if conftype not in nodes:
                nodes.append(conftype)
        # print(nodes)

        edges = []
        for edge in conferenceGraph.edges.data():
            source = edge[0][0:-4]
            target = edge[1][0:-4]
            if source == 'vldb':
                source = 'pvldb'

            if target == 'vldb':
                target = 'pvldb'

            edges.append((source, target, edge[2]['weight']))

        d={}
        for edge in edges:
            key = edge[0] + ',' + edge[1]
            if key not in d:
                d[key] = edge[2]
            else:
                d[key] += edge[2]
        # print(d.keys(), d.values())

        edges.clear()
        for edge, weight in d.items():
            source, target = edge.split(',')
            # print(source, target)
            edges.append((source, target, weight))
        # print(edges)

        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_weighted_edges_from(edges)

        self.conferenceDiGraph2 = graph


def FilterConferenceNodes(conferenceGraph, startyear=1950, endyear=2017, minTier=3, minSize=0):
    filteredNodes = []

    for node in conferenceGraph.nodes.data():
        if node[1]['year'] in list(range(startyear, endyear+1)):
            if node[1]['tier'] <= minTier:
                if node[1]['size'] >= minSize:
                    filteredNodes.append(node[0])

    conferenceSubGraph = conferenceGraph.subgraph(filteredNodes).copy()

    return conferenceSubGraph


# chris
def FilterAuthorNodes(authorGraph, startyear=1950, endyear=2019, min=1, max=4000, minSuccess = 0):
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


def GetDiGraphInDegreeStrengthPlot(graph):
    print(graph.in_degree(graph, weight='weight'))
    data = list(graph.in_degree(graph, weight='weight'))
    data.sort(key=lambda tup: tup[1], reverse=True)
    y_axis, x_axis = zip(*data)

    y_pos = np.arange(len(y_axis))

    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(y_axis, x_axis, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_axis)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_ylabel('Conference')
    ax.set_xlabel('in_degree Strength')
    ax.set_title('Movement Between Conferences')

    plt.savefig('ConferencesMovement.png')


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


def GetAuthorPublicationDistribution(authorGraph):
    # maxDegree = max(authorGraph.degree, key=lambda x: x[1])[1]
    # minDegree = min(authorGraph.degree, key=lambda x: x[1])[1]

    publication_seq = []
    for node in authorGraph.nodes.data():
        publication_seq.append(node[1]['size'])
    publication_seq = sorted(publication_seq, reverse=True)
    publicationCount = collections.Counter(publication_seq)

    publ, cnt = zip(*publicationCount.items())
    N = len(authorGraph.nodes)
    pk = []
    for publNum, cnt in publicationCount.items():
        pk.append(cnt/N)
    pk = sorted(pk)

    print(pk)
    print(publ)

    plt.figure()
    plt.scatter(publ, pk, c="r", s=10)

    plt.yscale('log')
    plt.xscale('log')

    # axes = plt.gca()
    # axes.set_xlim([0.9,max(publ)])
    # axes.set_ylim([min(pk)*0.1, 1])

    plt.scatter(publ, pk, c="r", s=10)

    plt.title("Author Publications Distribution")
    plt.ylabel("P(# Publications)")
    plt.xlabel("# Publications")
    plt.savefig("AuthorPublicationsDistribution.png")
    # graph too large to be drawn, but algorithms based on degree etc, can be done

    plt.close


def GetAuthorDegreeDistribution(graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    degList, degCountList = zip(*degreeCount.items())

    N = len(graph.nodes)
    pk = []
    for cnt in degCountList:
        pk.append(cnt/N)

    degList = sorted(degList)
    pk = sorted(pk, reverse=True)
    print(pk)
    print(degList)

    plt.figure()
    plt.scatter(degList, pk, c="r", s=10)

    plt.yscale('log')
    plt.xscale('log')

    axes = plt.gca()
    axes.set_xlim([0.9,max(degList)])
    axes.set_ylim([min(pk)*0.5, 1])

    plt.title("Author Degree Distribution")
    plt.ylabel("Pk")
    plt.xlabel("Degree")
    plt.savefig("AuthorDegreeDistribution.png")
    # graph too large to be drawn, but algorithms based on degree etc, can be done

    plt.close


def GetAuthorReputationDistributionPlot(graph):
    authorReputation = list(graph.nodes(data='reputation'))
    authorReputation.sort(key=lambda tup: tup[0], reverse=True)
    author, reputation = zip(*authorReputation)

    reputationCount = collections.Counter(reputation)
    reputationList, repCountList = zip(*reputationCount.items())

    pk = []
    N = len(authorReputation)
    for cnt in repCountList:
        pk.append(cnt/N)

    plt.figure()
    plt.scatter(reputationList, pk, c="r", s=10)

    plt.yscale('log')
    plt.xscale('log')

    # axes = plt.gca()
    # axes.set_xlim([0.9,max(degList)])
    # axes.set_ylim([min(pk)*0.1, 1])

    plt.scatter(reputationList, pk, c="r", s=10)

    plt.title("Author Reputation Distribution")
    plt.ylabel("P(Reputation)")
    plt.xlabel("Reputation")
    plt.savefig("AuthorReputationDistribution.png")
    # graph too large to be drawn, but algorithms based on degree etc, can be done

    plt.close



def GetAuthorReputationDegreePlot(graph):
    authorDegree = list(graph.degree())
    authorReputation = list(graph.nodes(data='reputation'))

    authorDegree.sort(key=lambda tup: tup[0], reverse=True)
    authorReputation.sort(key=lambda tup: tup[0], reverse=True)

    # print(len(authorDegree))
    # print(len(authorReputation))

    data = []
    for i in range(len(authorDegree)):
        data.append((authorReputation[i][1], authorDegree[i][1]))

    data.sort(key=lambda tup: tup[0], reverse=True)

    # print(data)

    y_axis, x_axis = zip(*data)
    # ax = plt.gca()
    plt.scatter(y_axis, x_axis, c="r", s=1)
    plt.title("Author Reputation vs. Degree")
    plt.ylabel("Reputation")
    plt.xlabel("Degree")
    # ax.set(xscale="log")
    # ax.set(yscale="log")
    plt.savefig("AuthorReputationDegree.png")
    plt.close


def GetAuthorPublicationDegreePlot(graph):
    authorDegree = list(graph.degree())
    authorPublication = list(graph.nodes(data='size'))

    authorDegree.sort(key=lambda tup: tup[0], reverse=True)
    authorPublication.sort(key=lambda tup: tup[0], reverse=True)

    # print(len(authorDegree))
    # print(len(authorReputation))

    data = []
    for i in range(len(authorDegree)):
        data.append((authorPublication[i][1], authorDegree[i][1]))

    data.sort(key=lambda tup: tup[0], reverse=True)

    # print(data)

    y_axis, x_axis = zip(*data)
    # ax = plt.gca()
    plt.scatter(y_axis, x_axis, c="r", s=1)
    plt.title("Author # Publications vs. Degree")
    plt.ylabel("# Publications")
    plt.xlabel("Degree")
    # ax.set(xscale="log")
    # ax.set(yscale="log")
    plt.savefig("AuthorPublicationDegree.png")
    plt.close


def PlotGraph(x, y, xLabel, yLabel, title):
    ax = plt.gca()
    ax.scatter(x, y, c="r")
    plt.title(title)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    ax.set(xscale="log")
    ax.set(yscale="log")
    plt.savefig(title + '.png')
    # graph too large to be drawn, but algorithms based on degree etc, can be done

    plt.close


def GetConferenceInDegreeStrength(conferenceGraph):
    d = {}
    for conf in conferenceGraph.nodes.data():
        in_degree = conferenceGraph.in_degree(conf[0], weight='weight')
        conftype = conf[0][0:-4]
        if conftype not in d:
            d[conftype] = [in_degree, 1]
        else:
            d[conftype][0] += in_degree
            d[conftype][1] += 1

    d['pvldb'][0] += d['vldb'][0]
    d['pvldb'][1] += d['vldb'][1]
    del d['vldb']

    data = []
    for k,v in d.items():
        data.append((k,v[0]))
    data.sort(key=lambda tup: tup[1], reverse=True)

    x_axis = [i[1] for i in data]
    y_axis = [i[0] for i in data]

    y_pos = np.arange(len(y_axis))

    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(y_axis, x_axis, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_axis)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_ylabel('Conference')
    ax.set_xlabel('in_degree')
    ax.set_title('Movement Between Conferences')

    plt.savefig('ConferencesMovement.png')

    return plt
