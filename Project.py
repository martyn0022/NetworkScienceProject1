import Preprocessing as ps
import NetworkGraph as ng
import Science as sc
from Interface import *
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


if __name__ == "__main__":
    main()
