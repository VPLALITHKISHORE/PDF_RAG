# app/main.py

from app.config import PDF_FOLDER, FAISS_PATH
from app.ingestion.loader import load_pdfs_parallel
from app.ingestion.chunker import chunk_documents
from app.embeddings.embedder import get_embeddings
from app.vectorstore.faiss_store import create_index, save_index, load_index
from app.retrieval.retriever import query

import os


def index_exists(path: str) -> bool:
    """Check if FAISS index files exist"""
    return os.path.exists(os.path.join(path, "index.faiss")) and \
           os.path.exists(os.path.join(path, "index.pkl"))


def build_index(embeddings):
    print("\n🚀 [STEP 1] Loading PDFs...")
    docs = load_pdfs_parallel(PDF_FOLDER)

    print(f"✅ Loaded {len(docs)} documents")

    print("\n🚀 [STEP 2] Chunking...")
    chunks = chunk_documents(docs)

    print(f"✅ Created {len(chunks)} chunks")

    print("\n🚀 [STEP 3] Creating FAISS index...")
    vectorstore = create_index(chunks, embeddings)

    print("\n🚀 [STEP 4] Saving index...")
    save_index(vectorstore, FAISS_PATH)

    print("✅ Index created successfully!\n")


def ask_question(embeddings):
    print("\n⚡ Loading FAISS index...")
    vectorstore = load_index(embeddings, FAISS_PATH)
    print("✅ Ready for queries!\n")

    while True:
        q = input("💬 Ask (type 'exit' to quit): ")

        if q.lower() == "exit":
            print("👋 Exiting...")
            break

        results = query(vectorstore, q)

        if not results:
            print("❌ No relevant results found.")
            continue

        for i, res in enumerate(results):
            print(f"\n--- Result {i+1} ---")
            print("📄 Source:", res.get("metadata", "N/A"))
            print("📝 Text:", res.get("text", "")[:300])


if __name__ == "__main__":
    print("🔧 Initializing embeddings...")
    embeddings = get_embeddings()

    try:
        if not index_exists(FAISS_PATH):
            print("⚠️ FAISS index not found. Building new index...")
            build_index(embeddings)
        else:
            print("✅ Existing FAISS index found.")

        ask_question(embeddings)

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("💡 Try deleting the FAISS folder and rebuilding.")