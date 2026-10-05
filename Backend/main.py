from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from uuid import uuid4
import os

from Backend.llm import llm
from Backend.database.mongo import db
from Backend.database.session_store import sessions
from Backend.database.interview_collection import interview_collection

from Backend.graph.start_graph import start_graph
from Backend.graph.submit_graph import submit_graph

from Backend.api.models import (
    SubmitAnswerRequest,
    StartInterviewRequest,
    StartInterviewSessionRequest
)

from Backend.rag.resume_parser import extract_resume_text
from Backend.rag.vector_store import store_resume_chunks, collection


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Mock Interviewer Backend Running"}


@app.get("/test-llm")
def test_llm():
    response = llm.invoke("Say hello in one line")
    return {"response": response.content}


@app.get("/test-db")
def test_db():
    collections = db.list_collection_names()
    return {"collections": collections}


@app.post("/create-session")
def create_session(request: StartInterviewRequest):
    session_id = str(uuid4())

    state = {
        "session_id": session_id,
        "role": request.role,
        "experience": request.experience,
        "interview_type": request.interview_type,
        "resume_uploaded": False,
        "current_question": "",
        "user_answer": "",
        "messages": [],
        "question_count": 0,
        "evaluation": {},
        "feedback": "",
        "interview_complete": False
    }

    sessions[session_id] = state

    interview_doc = {
        "session_id": session_id,
        "role": request.role,
        "experience": request.experience,
        "interview_type": request.interview_type,
        "history": [],
        "final_feedback": "",
        "created_at": datetime.utcnow()
    }

    interview_collection.insert_one(interview_doc)

    return {
        "session_id": session_id,
        "message": "Session created successfully"
    }


@app.post("/upload-resume")
def upload_resume(session_id: str, file: UploadFile = File(...)):
    if session_id not in sessions:
        return {"error": "Invalid session"}

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{session_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    resume_text = extract_resume_text(file_path)

    if not resume_text.strip():
        os.remove(file_path)
        return {"error": "Could not extract text from resume"}

    chunks_count = store_resume_chunks(session_id, resume_text)

    os.remove(file_path)

    sessions[session_id]["resume_uploaded"] = True

    return {
        "message": "Resume uploaded successfully",
        "chunks_stored": chunks_count
    }


@app.post("/start-interview")
def start_interview(request: StartInterviewSessionRequest):
    session_id = request.session_id

    if session_id not in sessions:
        return {"error": "Invalid session"}

    state = sessions[session_id]

    result = start_graph.invoke(state)
    sessions[session_id] = result

    return {
        "session_id": session_id,
        "question": result["current_question"]
    }


@app.post("/submit-answer")
def submit_answer(request: SubmitAnswerRequest):
    session_id = request.session_id

    if session_id not in sessions:
        return {"error": "Invalid session"}

    state = sessions[session_id]
    state["user_answer"] = request.answer

    current_question = state["current_question"]

    result = submit_graph.invoke(state)
    sessions[session_id] = result

    interview_collection.update_one(
        {"session_id": session_id},
        {
            "$push": {
                "history": {
                    "question": current_question,
                    "answer": request.answer,
                    "evaluation": result["evaluation"]
                }
            }
        }
    )

    if result["interview_complete"]:
        interview_collection.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "final_feedback": result["feedback"]
                }
            }
        )

        # cleanup
        collection.delete(where={"session_id": session_id})
        del sessions[session_id]

        return {
            "interview_complete": True,
            "feedback": result["feedback"]
        }

    return {
        "interview_complete": False,
        "next_question": result["current_question"]
    }