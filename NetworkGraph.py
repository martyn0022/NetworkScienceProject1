# requires installation
import collections

import networkx as nx
import matplotlib.pyplot as plt
import json


def SaveNodesEdgesinJSON (nodes, edges, fileName):
    with open('json/'+fileName+'Nodes.json', 'w') as json_file:
        json.dump(nodes, json_file)

    with open('json/'+fileName+'Edges.json', 'w') as json_file:
        json.dump(edges, json_file)


def ParseJSONtoDict (filename):
    # Read JSON data into the datastore variable
    if filename:
        with open(filename, 'r') as f:
            datastore = json.load(f)
    return datastore


class Network:
    def __init__ (self, JSONList):
        self.conferenceDetails = ParseJSONtoDict(JSONList[0])
        self.authors = ParseJSONtoDict(JSONList[1])
        self.inproceeds = ParseJSONtoDict(JSONList[2])
        # conferences are the nodes
        self.graph = nx.Graph()
        self.diGraph = nx.DiGraph()
        self.authGraph = nx.Graph()

    # def DrawGraph (self):
    #     maxW, minW, maxE, minE = self.AddNodesToNetwork()
    #     nodeWeight = []
    #     nodeColor = []
    #     edgeColors = []
    #     edges = []
    #
    #     for node in self.graph.nodes.data():
    #         nodeSize = node[1]['size']
    #         nodeSize = (nodeSize - minW) / (maxW-minW)
    #         nodeWeight.append(nodeSize*2000)
    #         nodeColor.append([1,1-nodeSize,1-nodeSize])
    #
    #     for edge in self.graph.edges.data():
    #         if int(edge[0][-4:]) < int(edge[1][-4:]):
    #             edgeWeight = edge[2]['weight']
    #             edgeWeight = (edgeWeight - minE) / (maxE - minE)
    #             edgeColors.append(edgeWeight*20)
    #             edges.append((edge[0],edge[1]))
    #
    #     plt.figure(figsize=(20,20))
    #     nx.draw_networkx(self.graph, with_labels=True, edgelist=edges,
    #                      node_size=nodeWeight, node_color=nodeColor,
    #                      edge_color=edgeColors, edge_cmap=plt.cm.Greys,
    #                      font_size=6)
    #     plt.savefig("test.png")
    #
    # # add range to filter
    # def AddNodesToNetwork (self):
    #     nodes = self.FilterNodes(2000, 2015)
    #     edges, nodesAttr, maxW, minW, maxE, minE = self.addEdgesToNetwork(nodes)
    #     self.graph.add_nodes_from(nodesAttr)
    #     self.graph.add_edges_from(edges)
    #     return maxW, minW, maxE, minE
    #
    # def addEdgesToNetwork (self, nodes):
    #     maxWeight = 0
    #     minWeight = 1000
    #     maxEdge = 0
    #     minEdge = 1000
    #     edges = []
    #     nodesAttr = []
    #
    #     for key1 in nodes:
    #         conf1 = key1[0]
    #         conf1year = key1[1]
    #         nodeWeight = 0
    #         for key2 in nodes:
    #             conf2 = key2[0]
    #             conf2year = key2[1]
    #             weight = 0
    #             if conf1 != conf2 and conf1year < conf2year:
    #                 for author1 in self.conferenceDetails[conf1]['authors']:
    #                     if author1 in self.conferenceDetails[conf2]['authors']:
    #                         weight += 1
    #                 edges.append((conf1, conf2, {'weight': weight}))
    #                 if weight >= 0:
    #                     if maxEdge < weight:
    #                         maxEdge = weight
    #                     if minEdge > weight:
    #                         minEdge = weight
    #             nodeWeight += weight
    #         nodesAttr.append((conf1, {'size': nodeWeight}))
    #         if nodeWeight >= 0:
    #             if maxWeight < nodeWeight:
    #                 maxWeight = nodeWeight
    #             if minWeight > nodeWeight:
    #                 minWeight = nodeWeight
    #     return edges, nodesAttr, maxWeight, minWeight, maxEdge, minEdge
    #
    # def FilterNodes (self, start, end):
    #     conferenceNodes = []
    #     for key, value in self.conferenceDetails.items():
    #         if int(value['year']) in list(range(start, end+1)) :
    #             conferenceNodes.append((key, int(value['year']), value['conftype'], int(value['tier']), len(value['authors'])))
    #     # print(conferenceNodes)
    #     return conferenceNodes

    def SaveNodesandEdges (self):
        self.CreateConfNodesEdges()
        self.CreateAuthNodesEdges()


    def CreateConfNodesEdges (self):
        conferenceNodes = []
        for key, value in self.conferenceDetails.items():
            conferenceNodes.append((key, int(value['year']), value['conftype'],
                                    int(value['tier']), len(value['authors'])))
        # print(conferenceNodes)

        confNodeAttr = []
        confEdge = []
        maxWeight = 0
        minWeight = 1000
        maxEdge = 0
        minEdge = 1000

        for key1 in conferenceNodes:
            conf1 = key1[0]
            conf1year = key1[1]
            nodeWeight = 0

            confNodeAttr.append((conf1, {'size': key1[4], 'tier': key1[3],
                                         'authors': self.conferenceDetails[conf1]['authors']}))

            for key2 in conferenceNodes:
                conf2 = key2[0]
                conf2year = key2[1]
                weight = 0
                if conf1 != conf2 and conf1year == conf2year-1:
                    # can use set and intersect
                    for author1 in self.conferenceDetails[conf1]['authors']:
                        if author1 in self.conferenceDetails[conf2]['authors']:
                            weight += 1
                    confEdge.append((conf1, conf2, weight))
                    if weight >= 0:
                        if maxEdge < weight:
                            maxEdge = weight
                        if minEdge > weight:
                            minEdge = weight
                nodeWeight += weight

            if nodeWeight >= 0:
                if maxWeight < nodeWeight:
                    maxWeight = nodeWeight
                if minWeight > nodeWeight:
                    minWeight = nodeWeight

        SaveNodesEdgesinJSON(confNodeAttr, confEdge,'conference')

    def CreateAuthNodesEdges (self):
        authNodes = []
        authEdges = []

        for key, value in self.authors.items():
            authNodes.append((key, {'size': len(value)}))

        for key, value in self.inproceeds.items():
            authors = value['authors']
            for author1 in authors:
                for author2 in authors:
                    if author1 != author2:
                        authEdges.append((author1,author2, {'tier': int(value['tier']), 'year':int(value['year'])}))

        SaveNodesEdgesinJSON(authNodes, authEdges,'author')


    def CreateConfDiGraph(self):
        nodesJSON = 'json/conferenceNodes.json'
        edgesJSON = 'json/conferenceEdges.json'
        if nodesJSON:
            with open(nodesJSON, 'r') as f:
                nodes = json.load(f)
        if edgesJSON:
            with open(edgesJSON, 'r') as f:
                edges = json.load(f)

        self.diGraph.add_nodes_from(nodes)
        self.diGraph.add_weighted_edges_from(edges)



    def DrawDiGraphConf(self, start, end):
        nodesJSON = 'json/conferenceNodes.json'
        edgesJSON = 'json/conferenceEdges.json'
        if nodesJSON:
            with open(nodesJSON, 'r') as f:
                nodes = json.load(f)
        if edgesJSON:
            with open(edgesJSON, 'r') as f:
                edges = json.load(f)

        nodeslist = []
        nodessize = {}
        edgeslist = []
        edgecolors = []

        for node in nodes:
            if int(node[0][-4:]) in list(range(start, end+1)):
                # print(node[0], self.diGraph.in_degree(node[0]))
                nodeslist.append(node[0])
                nodessize.update({node[0]: node[1]['size']})

        for edge in edges:
            if int(edge[0][-4:]) in list(range(start, end)):
                edgeWeight = edge[2]
                if edgeWeight > 0:
                    edgeslist.append((edge[0],edge[1],edgeWeight))

        self.diGraph.add_nodes_from(nodeslist)
        self.diGraph.add_weighted_edges_from(edgeslist)

        nodesize = list(nodessize.values())
        maxSize = max(nodesize)
        minSize = min(nodesize)
        maxNodeSize = 5000
        for size in nodesize:
            size = (size - minSize) / (maxSize -minSize) * maxNodeSize + 1000

        edgemax = max(edgeslist, key=lambda x: x[2])[2]
        edgemin = min(edgeslist, key=lambda x: x[2])[2]
        for edge in edgeslist:
            color = (edge[2] - edgemin) / (edgemax - edgemin)
            if color > 0.5:
                edgecolors.append(color)

        plt.figure(figsize=(20,20))
        pos=nx.spring_layout(self.diGraph, k=2)

        M = self.diGraph.number_of_edges()
        edge_colors = range(2, M + 2)
        edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

        nx.draw_networkx_nodes(
            self.diGraph, pos=pos,
            node_size=nodesize
        )

        edges = nx.draw_networkx_edges(
            self.diGraph,
            pos=pos,
            arrowstyle="->",
            arrowsize=5,
            edge_color=edge_colors,
            edge_cmap=plt.cm.Greys,
            width=1,
        )

        nx.draw_networkx_labels(
            self.diGraph, pos=pos, font_size=6,
            font_color='k', font_family='sans-serif',
            font_weight='normal', alpha=None,
            bbox=None, ax=None
        )

        # set alpha value for each edge
        for i in range(M):
            edges[i].set_alpha(edge_alphas[i])

        plt.savefig("conferenceNW.png")


    def CreateAuthGraph(self):
        nodesJSON = 'json/authorNodes.json'
        edgesJSON = 'json/authorEdges.json'
        if nodesJSON:
            with open(nodesJSON, 'r') as f:
                nodes = json.load(f)
        if edgesJSON:
            with open(edgesJSON, 'r') as f:
                edges = json.load(f)

        self.authGraph.add_nodes_from(nodes)
        self.authGraph.add_edges_from(edges)

        maxDegree = max(self.authGraph.degree, key=lambda x: x[1])[1]
        minDegree = min(self.authGraph.degree, key=lambda x: x[1])[1]

        degree_sequence = sorted([d for n, d in self.authGraph.degree()], reverse=True)
        degreeCount = collections.Counter(degree_sequence)
        deg, cnt = zip(*degreeCount.items())


        plt.figure()
        ax = plt.gca()
        ax.scatter(deg, cnt, c="r")
        
        plt.title("Author Degree Distribution")
        plt.ylabel("Count")
        plt.xlabel("Degree")

        # ax.set(xscale="log")
        ax.set(yscale="log")

        plt.savefig("AuthorDegreeDistribution.png")
        # graph too large to be drawn, but algorithms based on degree etc, can be done


    def CreateSubAuthGraph(self, startyear, endyear):
        subgraph = nx.Graph()
        nodelist = set()
        edgelist = set()

        for edge in self.authGraph.edges:
            if self.authGraph[edge[0]][edge[1]]['year'] in list(range(startyear, endyear+1))\
                    and self.authGraph[edge[0]][edge[1]]['tier'] == 3:
                edgelist.add(edge)
                nodelist.add(edge[0])
                nodelist.add(edge[1])

        subgraph.add_nodes_from(nodelist)
        subgraph.add_edges_from(edgelist)

        maxDegree = max(subgraph.degree, key=lambda x: x[1])[1]
        minDegree = min(subgraph.degree, key=lambda x: x[1])[1]


    def AuthorsReputation(self):
        authNodes = []
        authEdges = []
        authorsTier1 = []
        count = 0

        for author, publications in self.authors.items():
            count = 0
            authNodes.append((author, {'size': len(publications)}))
            for publ in publications:
                if publ['tier'] == 3:
                    count += 1
                authorsTier1.append((author, count))

        for key, value in self.inproceeds.items():
            authors = value['authors']
            for author1 in authors:
                for author2 in authors:
                    if author1 != author2:
                        authEdges.append((author1,author2, {'tier': int(value['tier']), 'year':int(value['year'])}))




