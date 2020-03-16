import collections
from operator import itemgetter
import json

import networkx as nx


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
