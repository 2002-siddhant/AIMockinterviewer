import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter


chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="resume_collection"
)


def store_resume_chunks(session_id, resume_text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(resume_text)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{session_id}_{i}"],
            metadatas=[{"session_id": session_id}]
        )

    return len(chunks)