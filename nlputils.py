import spacy
from spacy.language import Language
from typing import Optional

import baselog as log
from typing import List
from spacy.lang.en import English
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


def breakDoc(text:str):
    nlp = English()  # just the language with no pipeline
    nlp.add_pipe("sentencizer")
    doc = nlp(text)
    for sent in doc.sents:
        print(f"\n\n{sent.text}")

def testGetSentences():
    text = "sentence 1. Sentence 2. Sent"
    sentenceList = getSentences(text)
    log.ph("Sentence list", sentenceList)

def getASampleSonnet():
    sonnet = """
From fairest creatures we desire increase,
That thereby beauty’s rose might never die,
But as the riper should by time decease.
His tender heir might bear his memory:
But thou, contracted to thine own bright eyes,
Feed’st thy light’s flame with self-substantial fuel,
Making a famine where abundance lies.
Thyself thy foe, to thy sweet self too cruel:
Thou that art now the world’s fresh ornament,
And only herald to the gaudy spring,
Within thine own bud buriest thy content,
And tender churl mak’st waste in niggarding:
    Pity the world, or else this glutton be,
    To eat the world’s due, by the grave and thee.
"""
    return sonnet


def getSentencesFromSonnet(sonnet: str) -> List[str]:
    sentenceList = getSentences(sonnet)
    return sentenceList

def testGetSentencesSonnet():
    sonnet = getASampleSonnet()
    #sentenceList = getSentencesFromSonnet(sonnet)
    breakDoc(sonnet)
    #log.ph("Sentences in 1st sonnet", sentenceList)

def localTest():
    log.ph1("Starting local test")
    initialize()
    #testGetSentences()
    testGetSentencesSonnet()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()