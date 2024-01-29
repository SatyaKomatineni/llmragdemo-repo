"""
*******************************************
sdataset.py

1. shakespeare dataset.py
2. 1/29/24: No longer used

*******************************************
"""
import baselog as log
import nltk

from nltk.corpus import shakespeare

def initialize():
    log.ph1("Downloading dataset")
    nltk.download("shakespeare")
    log.dprint("Downloading dataset complete\n")

def parse_shakespeare_sonnets():
    sonnets = shakespeare.sonnets()  # Retrieve the Shakespeare sonnets dataset
    sonnet_list = sonnets.split("SONNET ")  # Split the full text into individual sonnets
    sonnet_dict = {}

    for sonnet in sonnet_list:
        sonnet = sonnet.strip()
        if sonnet:
            # Extract sonnet number and text
            lines = sonnet.split('\n')
            sonnet_number = int(lines[0].strip())
            sonnet_text = '\n'.join(lines[1:]).strip()
            sonnet_dict[sonnet_number] = sonnet_text

    return sonnet_dict

import nltk
from nltk.corpus import shakespeare
import re

def get_shakespeare_sonnets():

    # The 'shakespeare' corpus has multiple documents, including sonnets
    sonnets = shakespeare.xml('sonnets.xml')

    # Dictionary to store sonnet number and text
    sonnet_dict = {}

    # Iterate through each sonnet in the dataset
    for sonnet in sonnets.findall('.//sonnet'):
        # Extract sonnet number
        sonnet_number = sonnet.get('id')

        # Extract all lines of the sonnet
        lines = [line.text for line in sonnet.findall('.//line')]
        sonnet_text = ' '.join(lines)

        # Add to dictionary
        sonnet_dict[sonnet_number] = sonnet_text

    return sonnet_dict

def testDatasetLoad2():
    # Example usage
    sonnets = get_shakespeare_sonnets()
    print(sonnets['1'])  # Prints the text of Sonnet 1

def testDatasetLoad1():
    shakespeare_sonnets_dict = parse_shakespeare_sonnets()
    print(shakespeare_sonnets_dict[1])  # Print the first sonnet


def downloadShakespeareSonnets():

def localTest():
    log.ph1("Starting local test")
    initialize()
    testDatasetLoad2()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
