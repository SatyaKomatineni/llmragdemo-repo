
import chromadb
import baselog as log
import fileutils
import datasetutils
import nlputils
from typing import Tuple, List, Dict

sonnet_collection_name = "Test_Collection"

def getChromaClientPath():
    path = fileutils.getTempDataRoot()
    filename ="chromadb1"
    new_db_path = fileutils.pathjoin(path,filename)
    return new_db_path

def getChromaDBClient():
    chromadb_path = getChromaClientPath()
    chromadbClient = chromadb.PersistentClient(chromadb_path)
    return chromadbClient

def getOrCreateCollection(client: chromadb.ClientAPI, name: str):
    return client.get_or_create_collection(name)

def getOrCreateATestCollection() -> chromadb.Collection:
    #create chroma db
    log.ph1("Creating chromadb")
    chromaClient = getChromaDBClient()
    col = chromaClient.get_or_create_collection("Test_Collection")
    log.dprint("Get/Created test collection")
    return col

"""
**********************************************
Examine the database
**********************************************
"""
def examineCollection(col: chromadb.Collection):

    #Print collection name
    log.ph1(f"Examining collection: {col.name}")

    #Get the result (top 10 items)
    result = col.peek()
    
    #
    # result: 
    # Dictionary of ids, metadatas, documents, embeddings, uris
    #
    log.dprint(f"ids:{result['ids']}")
    log.dprint(f"\nMetadatas: {result['metadatas']}")
    log.dprint(f"\nuris: {result['uris']}")

    #Not printing docuemnts for they could be too large on a print
    #Same with embeddings

    #Print one document
    firstdoc = result["documents"][0]
    log.dprint(f"\n1st Document:\n\n{firstdoc}")

    return

def examineTestCollection():
    col = getOrCreateATestCollection()
    examineCollection(col)


"""
**********************************************
Populate the database
**********************************************
"""

def addASonnet(col: chromadb.Collection, sonnet: str, roman: str):
    log.validate_not_null_or_empty(col, sonnet, roman)
    id = datasetutils.roman_to_int(roman)
    id_str = f"{id}"
    mod_sonnet = getModifiedSonnet(sonnet,roman)
    #log.dprint(mod_sonnet)
    col.upsert(
        ids=[id_str],
        documents=[mod_sonnet],
        metadatas=[{"Sonnet number": id_str, "Sonnet Roman Numeral": roman}])
    return

def addASonnet2(col: chromadb.Collection, sonnet: str, roman: str):
    log.validate_not_null_or_empty(col, sonnet, roman)
    arrays = getSonnetVectorLists(sonnet, roman)
    col.upsert(
        ids=arrays[0],
        documents=arrays[1],
        metadatas=arrays[2]
    )
    return


def getSonnetVectorLists(sonnet: str, roman: str) -> Tuple[List[str], List[str], List[Dict[str,str]]]:
    doc1 = getSonnetSignature(roman)
    doc2 = sonnet
    doclist = [doc1, doc2]
    id = datasetutils.roman_to_int(roman)
    id1 = f"{id}"
    id2 = f"{id}_sonnet"
    idlist =[id1,id2]
    metadata1 = {"Sonnet number": id1, "Sonnet Roman Numeral": roman, "type":"number"}
    metadata2 = {"Sonnet number": id1, "Sonnet Roman Numeral": roman, "type":"sonnet"}
    metadatalist = [metadata1,metadata2]
    return [idlist,doclist,metadatalist]

def test_getSonnetVectorLists():
    sonnet = nlputils.getASampleSonnet()
    chromaDBLists = getSonnetVectorLists(sonnet, "I")
    log.dprint(f"\n{chromaDBLists[0]}")
    log.dprint(f"\n{chromaDBLists[1]}")
    log.dprint(f"\n{chromaDBLists[2]}")


def getSonnetSignature(romanNumeral: str):
    sonnet_number = datasetutils.roman_to_int(romanNumeral)
    s = """
Shakespeare wrote many sonnets. These sonnets have numbers.
This sonnet is: 
"""
    return f"{s} Sonnet {romanNumeral} or Sonnet {sonnet_number}.\n\n"

def getModifiedSonnet(sonnet: str, roman: str):
    #return f"{getSonnetSignature(roman)}{sonnet}"
    return f"{getSonnetSignature(roman)}"

def addFromASonnetDictionary(col: chromadb.Collection, sonnetsDict: dict):
    #key: roman numeral
    #value: sonnet
    for item in sonnetsDict.items():
        roman = item[0]
        sonnet = item[1]
        log.dprint(f"Adding sonnet:{roman}")
        #addASonnet(col,sonnet,roman)
        addASonnet2(col,sonnet,roman)
    return

def addSonnetDatasetToChromadb(reset_flag=False):

    if reset_flag == True:
        deleteTestCollection()

    log.ph1("Adding 20 sonnets to chromadb")

    #get sonnets
    log.dprint("Getting 20 sonnet dictionary")
    sonnetDict = datasetutils.get20SonnetsDictionary()
    log.summarizeDictionary(sonnetDict)

    #get a chromadb collection
    log.dprint("Get chromadb collection")
    col = getOrCreateATestCollection()

    log.dprint("Add sonnets")
    addFromASonnetDictionary(col,sonnetDict)

    log.ph1("Done with creating all sonnets")
    return

def deleteTestCollection():
    client = getChromaDBClient()
    global sonnet_collection_name
    log.ph("Deleting Collection",sonnet_collection_name)

    try :
        col = client.get_collection(sonnet_collection_name)
    except ValueError as e:
        log.dprint("test collection doesn't exist")
        return

    client.delete_collection(sonnet_collection_name)
    
def populateDatabase(reset_flag=False):
    addSonnetDatasetToChromadb(reset_flag)

"""
**********************************************
Querying
**********************************************
"""
def querySonnetsDB(queryText: str) -> chromadb.QueryResult: 
    log.validate_not_null_or_empty(queryText)
    col = getOrCreateATestCollection()
    results = col.query(
        query_texts=[queryText],
        n_results=1
    )
    return results

def examineQueryResult(results: chromadb.QueryResult):
    print(results)

def testQueries():
    #r = querySonnetsDB("I love Sonnet 4. So can you summarize Sonnet 1")
    #r = querySonnetsDB("Flowers")
    r = querySonnetsDB("Sap checked with frost")
    examineQueryResult(r)
    returnIdType = getSonnetIdType(r)
    if returnIdType == SonnetKeyType.No_key:
        log.info("No results found")
        return
    col = getOrCreateATestCollection()
    sonnet_text = getMatchingSonnetText(col,r)
    log.ph("Retrieved Sonnet", f"{sonnet_text}")

from enum import Enum
class SonnetKeyType(Enum):
    No_key = 0
    Key = 1
    Sonnet = 2

"""
3 cases:
1. None found
2. Sonnet key found
3. Sonnet found
"""
def getSonnetIdType(results: chromadb.QueryResult):
    id = getMatchingSonnetId(results)
    if id == None:
        log.warn("None found")
        return SonnetKeyType.No_key
    
    keyType = results["metadatas"][0][0]["type"]
    log.info(f"keytype: {keyType}")
    log.info(f"sonnet id:{id}")

    if keyType == "number":
        return SonnetKeyType.Key
   
    if keyType == "sonnet":
        return SonnetKeyType.Sonnet
    
    log.warn(f"Unknown key type: {keyType}")
    raise Exception(f"Unknown key type: {keyType}")

"""
**********************************************
Extracting sonnets
**********************************************
"""
def getMatchingSonnetId(results: chromadb.QueryResult) -> str:
    idlist = results["ids"][0]
    number_of_ids = len(idlist)
    firstDistance = results["distances"][0][0]

    if firstDistance > 1.5:
        log.warn(f"Distance is too large: {firstDistance} ")
        log.warn("returning none found")
        return None
    
    log.info(f"Distance: {firstDistance}")
    if number_of_ids > 1:
        log.warn("One id expected but got: {number_of_ids}")
        log.warn("picking up just the first one")
    firstid = idlist[0]
    log.info(f"SOnnet id: {firstid}")
    return firstid

def queryCollectionForSonnetById(col: chromadb.Collection, id: str) -> chromadb.QueryResult:
    newid = id.strip()
    sonnet_id = None
    if "sonnet" in newid:
        sonnet_id = newid
    else:
        sonnet_id = f"{newid}_sonnet"
    return col.get(
        ids=[sonnet_id],
        limit = 1
    )

def getFirstDocumentFromResult(results: chromadb.QueryResult):
    return results["documents"][0]

def getMatchingSonnetText(col: chromadb.Collection, results: chromadb.QueryResult) -> str:
    sonnet_number = getMatchingSonnetId(results)
    sonnet_results = queryCollectionForSonnetById(col, sonnet_number)
    sonnet_text = getFirstDocumentFromResult(sonnet_results)
    return sonnet_text


"""
**********************************************
Testing
**********************************************
"""

def testTestCollection():
    col: chromadb.Collection = getOrCreateATestCollection()
    addASonnet(col,"Sonnet One", "I")
    count = col.count()
    log.ph("Number of items in col", f"{count}")

def initialTest():
    chroma_client_path = getChromaClientPath()
    log.ph("Chroma db at", f"{chroma_client_path}")

    #create chroma db
    log.ph1("Creating chromadb")
    chromaClient = getChromaDBClient()
    log.dprint("Got chromadb client")

def localTest():
    log.ph1("Starting local test")
    #testTestCollection()
    #populateDatabase(True)
    #examineTestCollection()
    #test_getSonnetVectorLists()
    #deleteTestCollection()
    testQueries()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()