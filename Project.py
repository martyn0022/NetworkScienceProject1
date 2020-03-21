import Preprocessing as ps
import NetworkGraph as ng
import Science as sc
import json

conferenceAuthorJSON = "json/conferencesAndAuthors.json"
authorJSON = "json/authors.json"
inproceedsJSON = 'json/inproceeds.json'
dblpFilename = "DataScienceDBLP.xml"
listOfJSON = [conferenceAuthorJSON, authorJSON, inproceedsJSON]


def main ():
    # uncomment line below to preprocess dblp.xml again
    # ps.PreprocessConferencesAuthors(dblpFilename, listOfJSON)
    # uncomment line below to create new nodes and edges
    # ps.CreateNetworks()

    # inititalize networks class to create networkx graphs
    networks = sc.Networks()

    # filter author nodes, and create subgraph
    # authorSubGraph = sc.FilterAuthorNodes(networks.GetAuthorGraph(), startyear=2000, endyear=2002, minSuccess=0)

    # filter conference nodes, and create a subgraph
    # conferenceSubGraph = sc.FilterConferenceNodes(networks.GetConferenceGraph(), startyear=2000, endyear=2002)

    # calculate Degree Distribution
    # sc.GetDegreeDistribution(networks.GetAuthorGraph())

    # draw
    # sc.DrawGraph(conferenceSubGraph)

    # sc.CreateAuthorDistribution(networks.authorGraph)
    # PrintAuthorInformation(networks)
    # PrintConferenceInformation(networks)


if __name__ == "__main__":
    main()
