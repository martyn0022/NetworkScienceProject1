import xml
from typing import Dict
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import io
import csv
import re
import config as cfg

conferenceTier = cfg.conferenceTier
conferencesName = cfg.conferencesName
conferencesRegex = cfg.conferencesRegex

publicationsType = ["article", "book", "incollection",
                    "inproceedings", "mastersthesis", "phdthesis",
                    "proceedings", "www"]

publicationKeys = ["author", "title", "year", "volume",
                   "booktitle", "journal", "crossref"]

dataHeader = ["type", "confName", "key", "tier", "title", "year",
              "booktitle", "volume", "journal",
              "crossref"]

conferences = {}


def ParseDBLP ():
    parser = make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = DBLPHandler()
    parser.setContentHandler(Handler)
    print("PARSE1")
    parser.parse(io.open("DataScienceDBLP.xml"))
    '''
    with open('Inproceedings.csv', 'w', newline="", encoding='utf-8') as writeInproceed, \
            open('AuthorsInproceeding.csv', 'w', newline="", encoding='utf-8') as writeAuthor, \
            open('Proceedings.csv', 'w', newline="", encoding='utf-8') as writeProceed:
        inproceedWriter = csv.DictWriter(writeInproceed, fieldnames=dataHeader)
        inproceedWriter.writeheader()

        proceedWriter = csv.DictWriter(writeProceed, fieldnames=dataHeader)
        proceedWriter.writeheader()

        authorWriter = csv.writer(writeAuthor)
        authorWriter.writerow(["conference", "author"])

        parser.parse(io.open("DataScienceDBLP.xml"))

    writeInproceed.close()
    writeProceed.close()
    writeAuthor.close()
    '''
    return conferences


def AddToConference (conf, authors, year, conftype):
    if year not in conferences:
        conferences[year] = {conftype: {"author": authors, "name": conf}}
    elif year in conferences:
        if conftype not in conferences[year]:
            conferences[year][conftype] = {"author": authors, "name": conf}
        elif conftype in conferences[year]:
            conferences[year][conftype]["author"].extend(authors)


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
    currPublicationData = {"type": "NULL", "confName": "NULL", "key": "NULL", "tier": "NULL",
                           "title": "NULL", "year": "NULL",
                           "booktitle": "NULL", "volume": "NULL", "journal": "NULL",
                           "crossref": "NULL"}

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
                self.currPublicationData.update({"type": tag})

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

        # end of publication
        if tag == self.currentPublicationType and self.currentTypeOfConf in conferencesName:
            '''
            if self.currentPublicationType == "proceedings":
                conf = conferencesName[self.currentTypeOfConf] + " " + self.currPublicationData["year"]
                self.WriteAsProceedings(conf)
            '''
            if self.currentPublicationType == "inproceedings" or self.currentPublicationType == "article":
                self.WriteAsInproceedings()

            self.resetTemporaryVariables()

    # reset variables after every end of publication
    def resetTemporaryVariables (self):
        self.currPublicationAuthors.clear()
        self.currPublicationData = {"type": "NULL", "confName": "NULL", "key": "NULL", "tier": "NULL",
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
    def WriteAsInproceedings (self):
        year = self.currPublicationData["year"]
        conf = conferencesName[self.currentTypeOfConf] + " " + year
        crossref = self.currPublicationData["crossref"].lower()
        key = self.currPublicationData["key"].lower()
        authors = []
        writeBool = False

        if self.currentPublicationType == "inproceedings":
            if re.search("^conf/[a-z]+/[0-9]{2,4}(-[1-3])?$", crossref):
                if self.currentTypeOfConf == "sigmod":
                    print(self.currPublicationData["year"])
                writeBool = True
        elif self.currentPublicationType == "article":
            if re.search("^journals/pvldb/[a-zA-Z0-9]+$", key):
                writeBool = True

        if writeBool:
            self.currPublicationData.update({"confName": conf})
            for author in self.currPublicationAuthors:
                authors.append(author)
                # authorWriter.writerow([conf, author.replace("\n", "")])
            # store inproceeding/articles
            # inproceedWriter.writerow(self.currPublicationData)
            AddToConference(conf, authors, year, self.currentTypeOfConf)
