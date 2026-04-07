# app/ingestion/loader.py

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_core.documents import Document
from unstructured.partition.pdf import partition_pdf
from app.config import MAX_WORKERS


def load_single_pdf(file_path):
    elements = partition_pdf(
        filename=file_path,
        extract_tables=True,
        strategy="hi_res"
    )

    docs = []

    for el in elements:
        text = str(el).strip()
        if not text:
            continue

        metadata = {
            "source": os.path.basename(file_path),
            "type": str(type(el).__name__)
        }

        docs.append(Document(page_content=text, metadata=metadata))

    return docs


def load_pdfs_parallel(folder_path):
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".pdf")
    ]

    all_docs = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(load_single_pdf, f) for f in files]

        for future in as_completed(futures):
            try:
                all_docs.extend(future.result())
            except Exception as e:
                print("Error:", e)

    return all_docs