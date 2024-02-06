import hfdriver as aiutils
import baselog as log

from langchain_community.chat_models import ChatHuggingFace

#This import is important
#This allows pylance to recognize the type in this sentence
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

from langchain_core.outputs.llm_result import LLMResult

def getAHfLLM(token, endpoint):
    hf_ep = HuggingFaceEndpoint(
        endpoint_url=endpoint,
        huggingfacehub_api_token=token,
        task="text-generation"
    )
    return hf_ep

def getASampleHFEndPoint() -> HuggingFaceEndpoint:
    token = aiutils.getAPIKey()
    ep_url = aiutils.getSampleHFEndPoint()
    return getAHfLLM(token,ep_url)

def testEndPoint():
    llm = getASampleHFEndPoint()
    #Expects a list of strings
    reply =  llm.generate(["Are roses red?"])
    log.ph("Reply from LLM", f"{reply}")
    log.ph("Json from there", reply.json())
    getSingleTextFromHFEndPointReply(reply)
   
def getSingleTextFromHFEndPointReply(reply: LLMResult):
    output = reply.flatten()
    firstResult = output[0]
    log.ph("First", firstResult)
    firstGenList = firstResult.generations[0]
    log.ph("First Gen List", firstGenList)
    firstGen = firstGenList[0]
    log.ph("First Gen", firstGen)
    text = firstGen.text
    log.ph("First Gen text", text)
    return text


def localTest():
    log.ph1("Starting local test")
    testEndPoint()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()