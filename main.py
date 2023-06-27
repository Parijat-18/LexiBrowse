from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
import speech_recognition as sr
from speechToText import captureAudio
from langchain import PromptTemplate
from dotenv import load_dotenv
from textToSpeech import Speech
import json
import os
import msvcrt
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--save', type=bool, default=True, help='Saves the entire conversation in a json format.')
parser.add_argument('--nottp', action="store_false", help='Disables text to speech')

if __name__ == "__main__":

    def captureAudioThread(q):
        r = sr.Recognizer()
        while True:
            query = captureAudio(r)
            if query is not None:
                q.put(query)

    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
    
    template = """
    In order to generate an accurate and context-aware response, please consider the following sections:
    "
    1. Context: This section provides the background information or the general context that is relevant to the question. It is enclosed within the <ctx></ctx> tags.
    2. Chat History: This section contains the previous interactions or dialogues that have taken place. It is enclosed within the <hs></hs> tags. It's important to consider this to maintain the continuity and coherence of the conversation.
    3. Question: This is the query that needs to be addressed. 
    "
    After considering all these sections, please provide an appropriate answer.

    ------
    <ctx>
    {context}
    </ctx>
    ------
    <hs>
    {history}
    </hs>
    ------
    Question: {question}
    ------
    Answer:
    """

    prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=template,
    )
    args = parser.parse_args()
    load_dotenv()
    conversation_rec = []
    embedding = OpenAIEmbeddings(model=config['embedding_model'])
    openai = ChatOpenAI(temperature=0 , model=config['model'])
    vecDB = Chroma(persist_directory=config['persist_dir'] , embedding_function=embedding)
    query_chain = RetrievalQA.from_chain_type(llm=openai, 
                                              retriever=vecDB.as_retriever(), 
                                              return_source_documents=True,
                                              chain_type_kwargs={
                                                  "verbose":False,
                                                  "prompt":prompt,
                                                  "memory": ConversationBufferMemory(
                                                      memory_key="history",
                                                      input_key="question")
                                              }
                                        )
    r = sr.Recognizer()

    print('\033[92m' + "Greetings! Welcome to LexiBrowse. I am your AI-powered companion for swift and precise document exploration." + '\033[0m')

    typed_query = None
    spoken_query = None

    while True:
        if msvcrt.kbhit():
            typed_query = input('Enter your query: ')

        spoken_query = captureAudio(r)

        if typed_query:
            query = typed_query
            print(f"Your prompt: {query}")
        elif spoken_query:
            query = spoken_query
            print(f"Your prompt: {query}")

        if query != '/exit':
            llm_response = query_chain(query)
            if args.save:
                conversation = {
                    "user":query,
                    "lexi":llm_response['result']
                }
                conversation_rec.append(conversation)
            print('\033[92m' + "Lexi: " + '\033[0m' , llm_response['result'])
            print('sources: ')
            for source in llm_response['source_documents']:
                print(f"document: {source.metadata['source']} , Page Number: {source.metadata['page']}")
            if args.nottp == True:
                Speech(llm_response['result'])
            if args.save:
                with open('conversation.json', 'w') as f:
                    json.dump(conversation_rec, f , indent=4)
        else:   
            break

        typed_query = None
        spoken_query = None
        time.sleep(0.1) 
            

