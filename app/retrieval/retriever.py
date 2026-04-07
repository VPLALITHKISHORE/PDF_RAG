# app/retrieval/retriever.py

from app.config import TOP_K


def get_retriever(vectorstore):
    return vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )


def query(vectorstore, question):
    retriever = get_retriever(vectorstore)
    docs = retriever.get_relevant_documents(question)

    results = []
    for doc in docs:
        results.append({
            "text": doc.page_content,
            "metadata": doc.metadata
        })

    return results