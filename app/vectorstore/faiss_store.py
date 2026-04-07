# app/vectorstore/faiss_store.py

from langchain.vectorstores import FAISS


def create_index(chunks, embeddings):
    return FAISS.from_documents(chunks, embeddings)


def save_index(vectorstore, path):
    vectorstore.save_local(path)


def load_index(path, embeddings):
    return FAISS.load_local(path, embeddings)