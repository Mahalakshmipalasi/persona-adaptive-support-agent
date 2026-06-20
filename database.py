import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

DATA_DIR = "data"
DB_DIR = "data/faiss_index"

def initialize_knowledge_base():
    documents = []
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file)
        if file.endswith(".txt"):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

    if not documents:
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(DB_DIR)
    return vector_db

def get_vector_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(DB_DIR):
        return FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
    else:
        return initialize_knowledge_base()