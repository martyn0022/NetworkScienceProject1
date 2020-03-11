import Preprocessing as ps
import NetworkGraph as ng

conferenceAuthorJSON = "json/conferencesAndAuthors.json"
authorJSON = "json/authors.json"
inproceedsJSON = 'json/inproceeds.json'
dblpFilename = "DataScienceDBLP.xml"
listOfJSON = [conferenceAuthorJSON, authorJSON, inproceedsJSON]


def main ():
    # uncomment line below to preprocess dblp.xml again
    # ps.PreprocessConferencesAuthors(dblpFilename, listOfJSON)
    network = ng.Network(listOfJSON)
    # network.DrawGraph()

    # network.CreateConfNetwork()
    # network.CreateAuthNetwork()
    network.DrawDiGraphConf(2000,2005)
    network.DrawGraphAuth(2000,2005)


if __name__ == "__main__":
    main()
