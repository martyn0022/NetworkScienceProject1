import xml
from typing import Dict
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import io
import csv
import re
import config as cfg
import json
import pandas as pd

conferenceTier = cfg.conferenceTier
conferencesName = cfg.conferencesName
conferencesRegex = cfg.conferencesRegex

publicationsType = ["article", "book", "incollection",
                    "inproceedings", "mastersthesis", "phdthesis",
                    "proceedings", "www"]

publicationKeys = ["author", "title", "year", "volume",
                   "booktitle", "journal", "crossref"]

dataHeader = ["publtype", "conftype", "confName", "key", "tier", "title", "year",
              "booktitle", "volume", "journal",
              "crossref"]

dictionary = {}
conferences = {}
inproceeds = {}
authorsList = {}


def PreprocessConferencesAuthors (dblpFileName, JSONList):
    parser = make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = DBLPHandler()
    parser.setContentHandler(Handler)
    print("PARSE1")
    parser.parse(io.open(dblpFileName))

    with open(JSONList[0], 'w') as json_file:
        json.dump(conferences, json_file)

    with open(JSONList[1], 'w') as json_file:
        json.dump(authorsList, json_file)

    with open(JSONList[2], 'w') as json_file:
        json.dump(inproceeds, json_file)

    print("done parsing")
    return conferences


def AddToConference (key, conftype, year, tier, publauthors):
    authors = publauthors.copy()
    if key not in conferences:
        conferences[key] = {'key': key, 'conftype': conftype, 'year': year, 'tier': tier, 'authors': authors}
    elif key in conferences:
        conferences[key]['authors'].extend(authors)


def AddToInproceeds (key, crossref, conftype, year, tier, publauthors):
    authors = publauthors.copy()
    if key not in inproceeds:
        inproceeds[key] = {'key': key, 'conf':crossref, 'conftype':conftype, 'year':year, 'tier':tier, 'authors':authors}
        for author in authors:
            if author not in authorsList:
                authorsList[author] = [inproceeds[key]]
            else:
                authorsList[author].append(inproceeds[key])



def AddToData (publicationData, confType, publicationAuthors):
    conftype = confType
    tier = publicationData["tier"]
    year = publicationData["year"]
    confname = conferencesName[confType] + " " + year
    crossref = publicationData["crossref"].lower()
    key = publicationData["key"].lower()
    conferencekey = publicationData["conftype"] + publicationData["year"]
    writeBool = False

    if publicationData["publtype"] == "inproceedings":
        if re.search("^conf/[a-z]+/[0-9]{2,4}(-[1-3])?$", crossref):
            writeBool = True
    elif publicationData["publtype"] == "article":
        if re.search("^journals/pvldb/[a-zA-Z0-9]+$", key):
            writeBool = True

    if writeBool:
        publicationData.update({"confName": confname})
        AddToInproceeds(key, conferencekey, conftype, year, tier, publicationAuthors)
        AddToConference(conferencekey, conftype, year, tier, publicationAuthors)


class DBLPHandler(ContentHandler):
    # variables used to check publications
    currentTypeOfConf = ""
    currentPublicationType = ""
    currentTag = ""
    fullContent = ""
    listOfContent = ""
    isPublication = False

    # publication content, use for temporary storage per publication
    currPublicationAuthors = []
    currPublicationData = {"publtype": "NULL", "conftype": "NULL", "confName": "NULL", "key": "NULL", "tier": "NULL",
                           "title": "NULL", "year": "NULL",
                           "booktitle": "NULL", "volume": "NULL", "journal": "NULL",
                           "crossref": "NULL"}

    def __init__ (self):
        self.csv = CSVWriter()
        self.proceedWriter, self.inproceedWriter, self.authorWriter = self.csv.OpenCSVWriter()

    # Call when an element starts
    def startElement (self, tag, attrs):
        if tag == "dblp":
            return
        if tag in publicationsType:
            self.isPublication = True

            self.currentPublicationType = tag

            if "key" in attrs:
                value = attrs.get("key")
                valueArray = value.split('/')
                self.currentTypeOfConf = valueArray[1].lower()
                if self.currentTypeOfConf in conferencesName:
                    self.currPublicationData.update({"tier": conferenceTier[self.currentTypeOfConf]})
                self.currPublicationData.update({"key": value})
                self.currPublicationData.update({"publtype": tag})
                self.currPublicationData.update({"conftype": valueArray[1].lower()})

        # if inside a publication
        elif self.isPublication:
            self.currentTag = tag

    # Call when a character is read
    def characters (self, content):
        if self.isPublication and self.currentTypeOfConf in conferencesName and self.currentTag in publicationKeys:
            self.listOfContent += content

    # Call when ending tag found </example>
    def endElement (self, tag):
        if self.listOfContent != "":
            self.fullContent = self.listOfContent.strip().replace("\n", "")

        if self.isPublication and self.currentTypeOfConf in conferencesName and tag in publicationKeys:
            if tag == "author":
                self.currPublicationAuthors.append(self.fullContent)
            else:
                self.currPublicationData.update({tag: self.fullContent})

        self.fullContent = ""
        self.listOfContent = ""

        # end of publication, i.e. found </proceedings>
        if tag == self.currentPublicationType:
            if self.currentTypeOfConf in conferencesName:
                if self.currentPublicationType == "inproceedings" or self.currentPublicationType == "article":
                    AddToData(self.currPublicationData, self.currentTypeOfConf, self.currPublicationAuthors)
            self.resetTemporaryVariables()

        # end of dblp
        if tag == "dblp":
            self.csv.CloseCSVWriter()

    # reset variables after every end of publication
    def resetTemporaryVariables (self):
        self.currPublicationAuthors = []
        self.currPublicationData = {"publtype": "NULL", "confName": "NULL", "key": "NULL", "tier": "NULL",
                                    "title": "NULL", "year": "NULL",
                                    "booktitle": "NULL", "volume": "NULL", "journal": "NULL",
                                    "crossref": "NULL"}
        self.isPublication = False
        self.currentTypeOfConf = ""

    '''
    def WriteAsProceedings (self, conf):
        publicationTitle = self.currPublicationData["title"].lower()
        if self.currentTypeOfConf == "sigmod":
            if re.search("international conference on management of data", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        elif self.currentTypeOfConf in ["vldb", "pvldb"]:
            if re.search("international conference on very large (data bases|databases)", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        elif self.currentTypeOfConf == "kdd":
            if re.search("international conference on knowledge discovery (&|and) data mining", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        elif self.currentTypeOfConf == "edbt":
            if re.search("international conference on extending database technology", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        elif self.currentTypeOfConf == "icde":
            if re.search("international conference on data engineering", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        elif self.currentTypeOfConf == "icdm":
            if re.search("ieee(.*)international conference on data mining", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        elif self.currentTypeOfConf == "sdm":
            if re.search("siam international conference on data mining", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        elif self.currentTypeOfConf == "cikm":
            if re.search("conference on information and knowledge management", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        # some conferencesName are divided into parts <=3, conf/dasfaa/<year>-<1/2/3>
        elif self.currentTypeOfConf == "dasfaa":
            if re.search("database systems for advance(d|s) applications", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        # some conferencesName are divided into parts <=3, conf/pakdd/<year>-<1/2/3>
        elif self.currentTypeOfConf == "pakdd":
            if re.search("knowledge discovery and data mining(.*)pacific-asia conference", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        # some conferencesName are divided into parts <=3, conf/pkdd/<year>-<1/2/3>
        elif self.currentTypeOfConf == "pkdd":
            if re.search(
                    "(machine learning and )?knowledge discovery in databases|principles of data mining and knowledge discovery",
                    publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)

        # some conferencesName are divided into parts <=2, conf/dexa/<year>-<1/2/3>
        elif self.currentTypeOfConf == "dexa":
            if re.search("database and expert systems applications", publicationTitle):
                if re.search("(workshop|tutorial)", publicationTitle) is None:
                    self.currPublicationData.update({"confName": conf})
                    proceedWriter.writerow(self.currPublicationData)
    '''
class CSVWriter:
    def __init__ (self):
        self.inproceedWriter = None
        self.proceedWriter = None
        self.authorWriter = None
        self.writeInproceed = None
        self.writeAuthor = None
        self.writeProceed = None

    def OpenCSVWriter (self):
        with open('Inproceedings.csv', 'w', newline="", encoding='utf-8') as self.writeInproceed, \
                open('AuthorsInproceeding.csv', 'w', newline="", encoding='utf-8') as self.writeAuthor, \
                open('Proceedings.csv', 'w', newline="", encoding='utf-8') as self.writeProceed:
            self.inproceedWriter = csv.DictWriter(self.writeInproceed, fieldnames=dataHeader)
            self.inproceedWriter.writeheader()

            self.proceedWriter = csv.DictWriter(self.writeProceed, fieldnames=dataHeader)
            self.proceedWriter.writeheader()

            self.authorWriter = csv.writer(self.writeAuthor)
            self.authorWriter.writerow(["conference", "author"])
        return self.inproceedWriter, self.proceedWriter, self.authorWriter

    def CloseCSVWriter (self):
        self.writeInproceed.close()
        self.writeAuthor.close()
        self.writeProceed.close()
