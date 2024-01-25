import spacy
from spacy.language import Language
from typing import Optional

import baselog as log
from typing import List
#import nltk

nlpmodel: Language

def initialize():
    global nlpmodel
    nlpmodel = spacy.load("en_core_web_sm")

def getSentences(paragraph: str):
    global nlpmodel
    doc = nlpmodel(paragraph)
    return [sent for sent in doc.sents]

def getAtMostSentences(sentenceList, max):
    s: str = ""
    count = 0
    for sent in sentenceList:
        if count == max:
            return s
        s = f"{s} {sent}"
        count = count + 1
    return s


def testGetSentences():
    text = "sentence 1. Sentence 2. Sent"
    sentenceList = getSentences(text)
    log.ph("Sentence list", sentenceList)

def localTest():
    log.ph1("Starting local test")
    initialize()
    testGetSentences()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()