# app/main.py

from app.config import PDF_FOLDER, FAISS_PATH
from app.ingestion.loader import load_pdfs_parallel
from app.ingestion.chunker import chunk_documents
from app.embeddings.embedder import get_embeddings
from app.vectorstore.faiss_store import create_index, save_index, load_index
from app.retrieval.retriever import query

import os


def build_index():
    print("Loading PDFs...")
    docs = load_pdfs_parallel(PDF_FOLDER)

    print("Chunking...")
    chunks = chunk_documents(docs)

    print("Embedding...")
    embeddings = get_embeddings()

    print("Creating FAISS index...")
    vectorstore = create_index(chunks, embeddings)

    print("Saving index...")
    save_index(vectorstore, FAISS_PATH)


def ask_question():
    embeddings = get_embeddings()
    vectorstore = load_index(FAISS_PATH, embeddings)

    while True:
        q = input("\nAsk: ")
        if q.lower() == "exit":
            break

        results = query(vectorstore, q)

        for i, res in enumerate(results):
            print(f"\n--- Result {i+1} ---")
            print("Source:", res["metadata"])
            print("Text:", res["text"][:300])


if __name__ == "__main__":
    if not os.path.exists(FAISS_PATH):
        build_index()

    ask_question()