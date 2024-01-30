import chromadb
import baselog as log
import fileutils
import datasetutils

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
    col.upsert(
        ids=[id_str],
        documents=[sonnet],
        metadatas=[{"Sonnet number": id_str, "Sonnet Roman Numeral": roman}])
    return

def addFromASonnetDictionary(col: chromadb.Collection, sonnetsDict: dict):
    #key: roman numeral
    #value: sonnet
    for item in sonnetsDict.items():
        roman = item[0]
        sonnet = item[1]
        log.dprint(f"Adding sonnet:{roman}")
        addASonnet(col,sonnet,roman)
    return

def addSonnetDatasetToChromadb():
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

def populateDatabase():
    addSonnetDatasetToChromadb()

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
    #populateDatabase()
    examineTestCollection()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()