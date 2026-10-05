from rag.retriever import retrieve_resume_context

context = retrieve_resume_context("projects", "test123")

print(context)