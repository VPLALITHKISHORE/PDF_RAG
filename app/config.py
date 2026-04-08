import os

PDF_FOLDER = "data/pdfs"
FAISS_DIR = "data/faiss_index"

FAISS_PATH = os.path.join(FAISS_DIR, "index.faiss")
METADATA_PATH = os.path.join(FAISS_DIR, "metadata.pkl")
TRACKER_PATH = os.path.join(FAISS_DIR, "processed_files.json")

API_KEY = "your-api-key"

EMBEDDING_API_URL = "https://your-embedding-endpoint"
CHAT_API_URL = "https://your-chat-endpoint"

EMBEDDING_MODEL = "embedding-model"
CHAT_MODEL = "chat-model"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 4
BATCH_SIZE = 32