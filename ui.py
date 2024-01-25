import baselog as log
import hfdriver as hfd
import requests
import httputils as http
import spacy
import nlputils

def printHeading():
    log.uph1("Application: Testing Text Generation Model from Hugging face")


def execute_prompt_loop():
    while True:
        user_input = log.prompt("Ask me a question (type 'q' or 'quit' to exit): ")
        
        l_user_input = user_input.lower()
        if l_user_input == 'q' or user_input == 'quit':  # Check if the input is 'q' or 'quit' (case-sensitive)
            print("Exiting the program.")
            break

        process_prompt(user_input)

def process_prompt(prompt):
    # Add your processing logic here
    params = hfd.getParameters()
    print(f"You entered: {prompt}")
    response: requests.Response = hfd.queryModel(prompt,params)
    response.raise_for_status()
    answer: str = http.getHFSingleGeneratedText(response)
    log.ph("Answer", answer)
    sentenceList = nlputils.getSentences(answer)
    finalAnswer = nlputils.getAtMostSentences(sentenceList,2)
    log.uph("Answer", finalAnswer)


def initialize():
    log.turnOffDebug()
    nlputils.initialize()

def main():
    initialize()
    printHeading()
    execute_prompt_loop()

main()

