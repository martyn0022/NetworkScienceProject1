import Preprocessing as ps
import NetworkGraph as ng
import Science as sc

conferenceAuthorJSON = "json/conferencesAndAuthors.json"
authorJSON = "json/authors.json"
inproceedsJSON = 'json/inproceeds.json'
dblpFilename = "DataScienceDBLP.xml"
listOfJSON = [conferenceAuthorJSON, authorJSON, inproceedsJSON]


def main ():
    # uncomment line below to preprocess dblp.xml again
    # ps.PreprocessConferencesAuthors(dblpFilename, listOfJSON)
    ps.CreateNetworks()

    ## network = ng.Network(listOfJSON)
    # network.SaveNodesandEdges()
    # network.CreateDiGraphConf(2000,2005)
    ## network.CreateAuthGraph()
    # network.CreateSubAuthGraph(2001,2001)

    # network = sc.Networks()



if __name__ == "__main__":
    main()
