import XMLParser as ps
import NetworkGraph as ng
import json

conferenceAuthorJSON = "conferencesAndAuthors.json"
dblpFilename = "DataScienceDBLP.xml"


def main ():
    # uncomment line below to re-preprocess dblp
    # ps.PreprocessConferencesAuthors(dblpFilename, conferenceAuthorJSON)
    conferences = ParseJSONtoDict(conferenceAuthorJSON)
    network = ng.Network(conferences)
    network.DrawGraph()


def ParseJSONtoDict (filename):
    # Read JSON data into the datastore variable
    if filename:
        with open(filename, 'r') as f:
            datastore = json.load(f)
    return datastore


if __name__ == "__main__":
    main()
