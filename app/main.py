import os
from app.config import *
from app.ingestion.loader import load_pdf_stream
from app.ingestion.chunker import chunk_text
from app.embeddings.embedder import embed_batch
from app.vectorstore.faiss_store import create_or_load_index, add_to_index, save_index
from app.retrieval.retriever import retrieve
from app.llm.chat import generate_answer
from app.utils.tracker import load_processed_files, save_processed_files


def update_index():
    print("⚡ Checking for new PDFs...")

        processed_files = load_processed_files(TRACKER_PATH)

            all_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
                new_files = [f for f in all_files if f not in processed_files]

                    if not new_files:
                            print("✅ No new PDFs found.")
                                    return

                                        print("📄 New files:", new_files)

                                            index, metadata = create_or_load_index(FAISS_PATH, METADATA_PATH)

                                                batch_texts = []
                                                    batch_meta = []

                                                        for file in new_files:
                                                                file_path = os.path.join(PDF_FOLDER, file)

                                                                        print(f"🚀 Processing {file}")

                                                                                for page in load_pdf_stream(file_path):
                                                                                            for chunk in chunk_text(page["text"], CHUNK_SIZE, CHUNK_OVERLAP):

                                                                                                            batch_texts.append(chunk)
                                                                                                                            batch_meta.append({
                                                                                                                                                "text": chunk,
                                                                                                                                                                    "metadata": page["metadata"]
                                                                                                                                                                                    })

                                                                                                                                                                                                    if len(batch_texts) >= BATCH_SIZE:
                                                                                                                                                                                                                        embeddings = embed_batch(batch_texts)

                                                                                                                                                                                                                                            index = add_to_index(index, embeddings)
                                                                                                                                                                                                                                                                metadata.extend(batch_meta)

                                                                                                                                                                                                                                                                                    batch_texts, batch_meta = [], []

                                                                                                                                                                                                                                                                                            processed_files.add(file)

                                                                                                                                                                                                                                                                                                if batch_texts:
                                                                                                                                                                                                                                                                                                        embeddings = embed_batch(batch_texts)
                                                                                                                                                                                                                                                                                                                index = add_to_index(index, embeddings)
                                                                                                                                                                                                                                                                                                                        metadata.extend(batch_meta)

                                                                                                                                                                                                                                                                                                                            save_index(index, metadata, FAISS_PATH, METADATA_PATH)
                                                                                                                                                                                                                                                                                                                                save_processed_files(TRACKER_PATH, processed_files)

                                                                                                                                                                                                                                                                                                                                    print("✅ Index updated successfully!")


                                                                                                                                                                                                                                                                                                                                    def chat_loop():
                                                                                                                                                                                                                                                                                                                                        index, metadata = create_or_load_index(FAISS_PATH, METADATA_PATH)

                                                                                                                                                                                                                                                                                                                                            if index is None:
                                                                                                                                                                                                                                                                                                                                                    print("❌ No index found. Add PDFs first.")
                                                                                                                                                                                                                                                                                                                                                            return

                                                                                                                                                                                                                                                                                                                                                                while True:
                                                                                                                                                                                                                                                                                                                                                                        q = input("\n💬 Ask: ")
                                                                                                                                                                                                                                                                                                                                                                                if q.lower() == "exit":
                                                                                                                                                                                                                                                                                                                                                                                            break

                                                                                                                                                                                                                                                                                                                                                                                                    docs = retrieve(q, index, metadata)
                                                                                                                                                                                                                                                                                                                                                                                                            answer = generate_answer(q, docs)

                                                                                                                                                                                                                                                                                                                                                                                                                    print("\n🤖 Answer:\n", answer)


                                                                                                                                                                                                                                                                                                                                                                                                                    if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                                                                                                        update_index()
                                                                                                                                                                                                                                                                                                                                                                                                                            chat_loop()