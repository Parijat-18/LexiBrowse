import os
from langchain.vectorstores import Chroma
from tiktoken import get_encoding
from langchain.document_loaders import PyPDFDirectoryLoader , PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def fileDirToDoc(input_dir='resources\pdf_files'):
    if os.path.exists(input_dir):
        loader = PyPDFDirectoryLoader(input_dir , glob='./*.pdf')
        doc = loader.load()
        return doc
    else:
        print('Input Path Doesnt exist')

def linkToDoc(pdf_links):
    doc = []
    for pdf_link in pdf_links:
        if pdf_link != '':
            try:
                loader = PyPDFLoader(pdf_link)
                tmp_doc = []
                for each_page in loader.load():
                    each_page.metadata['source'] = pdf_link
                    tmp_doc.append(each_page)
                doc += tmp_doc
            except Exception as e:
                print(f"An error occurred while scraping the pdf link {pdf_link}): {e}")
    return doc

def docToChunks(doc , chunk_size=1000 , chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size , chunk_overlap=chunk_overlap)
    texts = splitter.split_documents(doc)
    return texts

def setupPersistChromaDB(texts , embedding_model="text-embedding-ada-002", persist_directory='resources/db'):
    enc = get_encoding("cl100k_base")
    embedding =  OpenAIEmbeddings(model=embedding_model , disallowed_special=(enc.special_tokens_set - {'<|endofprompt|>'}))
    vecDB = Chroma.from_documents(documents=texts , embedding=embedding , persist_directory=persist_directory)
    vecDB.persist()


if __name__ == "__main__":
    pass