from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    role: str
    experience: str
    interview_type: str


class StartInterviewSessionRequest(BaseModel):
    session_id: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    answer: str