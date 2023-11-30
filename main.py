from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from textToSpeech import Speech
from speechToText import start_recording
import openai
import argparse
import json
import os


if __name__ == "__main__":
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', type=bool, default=True, help='Saves the entire conversation in a json format.')
    parser.add_argument('--persist_dir', type=str, default=config['persist_dir'], help='Path to the location of your persisted Chroma database')
    parser.add_argument('--savetts', action="store_true", help='Saves the streamed audio files.')
    parser.add_argument('--docs', type=int , default=6, help='Choose number of chunks to cite')
    parser.add_argument('--notts', action="store_true", help='Disables text to speech')
    parser.add_argument('--model', type=str, default=config['model'], help='Select the model from OpenAI API')

    
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
    count = 1
    embedding = OpenAIEmbeddings(model=config['embedding_model'])
    llm = ChatOpenAI(temperature=0.2 , model=args.model)
    vecDB = Chroma(persist_directory=args.persist_dir , embedding_function=embedding)
    query_chain = RetrievalQA.from_chain_type(llm=llm,
                                              retriever=vecDB.as_retriever(search_kwargs={"k":args.docs}), 
                                              return_source_documents=True,
                                              chain_type_kwargs={
                                                  "prompt":prompt,
                                                  "memory": ConversationBufferMemory(
                                                      memory_key="history",
                                                      input_key="question",
                                                      max_token_limit=1000)
                                              }
                                        )

    print('\033[92m' + "Greetings! Welcome to LexiBrowse. I am your AI-powered companion for swift and precise document exploration." + '\033[0m')

    while True:
        
        if args.notts == False:
            print("To speak to lexi press ctrl + alt + l and ask your question, after which press s")
            query = start_recording()
            print(f'Your Query: {query}')
        else:
            query = input('Enter your query: ')
        if query != 'stop':
            llm_response = query_chain(query)
            print('\033[92m' + "Lexi: " + '\033[0m' , llm_response['result'])
            print('sources: ')
            for source in llm_response['source_documents']:
                print(f"document: {source.metadata['source']} , Page Number: {source.metadata['page']}")

            if args.save:
                conversation = {
                    "user":query,
                    "lexi":llm_response['result']
                }

            if args.notts == False:
                if args.savetts:
                    audio_file = f"speechFiles\\audio{count}.wav"
                    Speech(llm_response['result'] , audio_file)
                    conversation['audio_path'] = audio_file
                    count += 1
                else:
                    Speech(llm_response['result'])

            if args.save:
                if os.path.exists('config.json'):
                    with open('conversation.json', 'r') as f:
                        conversation_rec = json.load(f)

                conversation_rec.append(conversation)

                with open('conversation.json', 'w') as f:
                    json.dump(conversation_rec, f, indent=4)
        else:   
            break

            

