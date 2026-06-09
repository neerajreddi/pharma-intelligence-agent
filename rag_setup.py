import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

def create_vector_database():
    print("Loading medical documents...")
    
    documents = []
    pdf_folder = "medical_docs"
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            print(f"Loading: {filename}")
            loader = PyPDFLoader(os.path.join(pdf_folder, filename))
            documents.extend(loader.load())
    
    print(f"Total pages loaded: {len(documents)}")
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    
    # Create embeddings and store in ChromaDB
    print("Creating vector database...")
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    print("Vector database created successfully!")
    return vectordb

if __name__ == "__main__":
    create_vector_database()