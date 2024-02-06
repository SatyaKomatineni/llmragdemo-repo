import os
import requests
import baselog as log
import httputils as http

HuggingFace_API_Env_key = "HUGGINGFACE_API_KEY"
#API_URL = "https://huggingface.co/HuggingFaceH4/zephyr-7b-beta" 
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
FB_API_URL ="https://z8dvl7fzhxxcybd8.eu-west-1.aws.endpoints.huggingface.cloud/"

def getEnvVariable(name, default):
    value = os.environ[name] 
    if value == None:
        return default
    return value

def getAPIKey():
    API_Key = getEnvVariable(HuggingFace_API_Env_key, None)
    if API_Key == None:
        raise Exception(f"No api key found in environment:{HuggingFace_API_Env_key}")
    return API_Key

def getSampleHFEndPoint():
    return "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    
"""
**************************
Type of response object: <class 'requests.models.Response'>
Type of Headers: <class 'requests.structures.CaseInsensitiveDict'>
Type of payload: <class 'str'>

If JSON, it can be a list of jsons
Returns a list of dictionaries
**************************
"""
def queryModel(prompt, parameters):
    apiKey = getAPIKey()
    headers = {"Authorization": f"Bearer {apiKey}"}
    payload = {
        "inputs": prompt,
        "parameters": parameters
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    http.understandResponse(response)
    return response

def extractGeneratedText(response: requests.Response):
    return response.json()[0]['generated_text']

def getParameters1():
    return {
            "max_new_tokens": 200,
            "temperature": 0.6,
            "top_p": 0.9,
            "do_sample": False,
            "return_full_text": False
    }

def getParameters():
    return {
        "max_length": 200
    }



def getTestPrompt():
    question = "What is the population of Jacksonville, Florida?"
    return question

def getTestPrompt2():
    question = "What is the population of Jacksonville, Florida?"
    context = "As of the most current census, Jacksonville, Florida has a population of 1 million."
    prompt = f"""Use the following context to answer the question at the end.
    {context}
    Question: {question}
    """
    return prompt

def testModel():
    prompt = getTestPrompt()
    log.ph("Prompt",prompt)
    params = getParameters()
    response: requests.Response = queryModel(prompt,params)
    response.raise_for_status()
    answer: str = http.getHFSingleGeneratedText(response)
    log.ph("Final Answer", answer)

def testAPIKey():
    s = getAPIKey()
    log.ph("key",s)

def test():
    #log.ph("hello", "hello")
    testModel()
    
#run
if __name__ == '__main__':
    test()