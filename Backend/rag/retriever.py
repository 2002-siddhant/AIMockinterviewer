from Backend.rag.vector_store import collection


def retrieve_resume_context(query, session_id):
    results = collection.query(
        query_texts=[query],
        n_results=3,
        where={"session_id": session_id}
    )

    documents = results["documents"][0]

    context = "\n".join(documents)

    return context