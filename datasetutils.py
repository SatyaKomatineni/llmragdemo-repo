"""
***************************************************
Backlog:

1/29/24
1. Load full sonnet set
2. Provide robust error handling while reading datasets
3. Do checks and balances of what is expected in each step
***************************************************
"""

import baselog as log
import nltk
import requests
import fileutils
import re


"""
***************************************************
Most useful functions
***************************************************
"""

"""
***************************************************
Name: get20SonnetsDictionary()

1. Return the first 20 sonnets as a dictionary
2. key: Roman numeral
3. Value: Sonnet text
***************************************************
"""
def get20SonnetsDictionary():
    filepath = fileutils.getSonnetFilepath("small-sonnets-10.txt")
    sonnets_text = fileutils.read_text_file(filepath)
    sonnetDictionary = convert_sonnets_text_to_dictinoary(sonnets_text)
    return sonnetDictionary

"""
1. Downloads /users/user/appdata/roaming/shakespeare
2. You may then want to move them to a certain local directory
3. This data set at the moment has a few play in them
4. does not contain the sonnets
"""
def loadNltkShakespeareDS():
    log.ph1("Downloading nltk shakespeare dataset")
    nltk.download("shakespeare")
    log.dprint("Downloading dataset complete\n")

"""
***************************************************
1. This doesn't work
2. No good data sets out there
3. Not sure anymore if this works
4. I did download manually that file 
5. It is kept in the /datasets/sonnets directory
6. I also downloaded sonnets-gutenberg.txt manually
7. It is saved in the same place
***************************************************
"""
def loadSonnets(filepath: str):
    url_bad = "https://www.gutenberg.org/files/1041/1041.txt"
    url = "https://github.com/martin-gorner/tensorflow-rnn-shakespeare/blob/master/shakespeare/sonnets.txt"
    response = requests.get(url)
    text = response.text
    log.examine_large_string(text,200,"Shakespeare sonnets")
    log.validate_not_null_or_empty("Loaded sonnets text", text)

    log.ph1("Savings sonnets file")
    fileutils.save_text_to_file(text,filepath)
    log.dprint("Successfuly saved: {filepath}")



"""
***************************************************
Parse sonnets
***************************************************
"""
def roman_to_int(roman):
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    num = 0
    prev_value = 0
    for char in reversed(roman):
        value = roman_numerals[char]
        if value < prev_value:
            num -= value
        else:
            num += value
        prev_value = value
    return num

def convert_sonnets_text_to_dictinoary(text):
    roman_numeral_pattern = r'\n(\b[IVXLCDM]+\b)\n'

    # Split the text by Roman numerals
    segments = re.split(roman_numeral_pattern, text)
    log.dprint(f"Segments: {len(segments)}")
    #examineSegments(segments,1)

    newsegments = segments[1:]
    #examineSegments(newsegments,2)

    pairedList = list_to_pairs(newsegments)
    #log.ph("Paired list", pairedList)

    sonnet_dict = list_to_dict(newsegments)
    #log.ph("Dictionary", sonnet_dict)

    return sonnet_dict

             
    

def list_to_pairs(lst):
    return [lst[i:i+2] for i in range(0, len(lst), 2)]

def list_to_dict(lst):
    return {lst[i]:lst[i+1].strip() for i in range(0, len(lst), 2)}

def examineSegments(segList, context):
    log.ph1(f"Examining segments :{context}")
    for id, seg in enumerate(segList):
        log.dprint(f"Seg {id}: {seg}")
    

"""
*****************************************************
Tests a simple sonnet file
1. a small file with 3 sonnet segments
2. Use it to test the logic
*****************************************************
"""
def testSonnets():
    #sonnets_text = fileutils.read_text_file("./datasets/small-sonnets.txt")
    sonnets_text = fileutils.read_text_file("./datasets/small-sonnets-2.txt")
    sonnetD = process_text(sonnets_text)
    """
    for key, value in sonnetD.items():
        print(f"{key}:\n{value}\n")
    """
"""
*****************************************************
Tests a key method that returns 20 sonnets
*****************************************************
"""
def testSonnets2():
    d = get20SonnetsDictionary()
    log.summarizeDictionary(d)

def localTest():
    log.ph1("Starting local test")
    #testSonnets()
    testSonnets2()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()