# app/vectorstore/faiss_store.py

from langchain_community.vectorstores import FAISS

def create_index(documents, embeddings):
    return FAISS.from_documents(documents, embeddings)

def save_index(db, path="faiss_index"):
    db.save_local(path)

def load_index(embeddings, path="faiss_index"):
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)