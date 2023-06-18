from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def fileDirToDoc(input_dir='resources\pdf_files'):
    loader = PyPDFDirectoryLoader(input_dir , glob='./*.pdf')
    doc = loader.load()
    return doc


def docToChunks(doc , chunk_size=1000 , chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size , chunk_overlap=chunk_overlap)
    texts = splitter.split_documents(doc)
    return texts

def setupPersistChromaDB(texts , embedding_model="text-embedding-ada-002", persist_directory='resources/db'):
    embedding =  OpenAIEmbeddings(model=embedding_model)
    vecDB = Chroma.from_documents(documents=texts , embedding=embedding , persist_directory=persist_directory)
    vecDB.persist()


if __name__ == "__main__":
    pass