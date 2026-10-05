from typing import TypedDict, List, Dict


class InterviewState(TypedDict):
    session_id: str
    role: str
    experience: str
    interview_type: str
    resume_uploaded: bool
    current_question: str
    user_answer: str
    messages: List[str]
    question_count: int
    evaluation: Dict
    feedback: str
    interview_complete: bool