from Backend.llm import llm
from Backend.rag.retriever import retrieve_resume_context


def question_generator(state):
    print("Question Generator Running...")

    role = state["role"]
    experience = state["experience"]
    interview_type = state["interview_type"]

    session_id = state.get("session_id")
    resume_uploaded = state.get("resume_uploaded", False)
    question_count = state["question_count"]

    resume_context = ""

    if resume_uploaded:
        if question_count % 3 == 0:
            query = "projects"
        elif question_count % 3 == 1:
            query = "skills"
        else:
            query = "technical experience"

        resume_context = retrieve_resume_context(query, session_id)

    if resume_uploaded and resume_context:
        prompt = f"""
You are an expert technical interviewer.

Generate one interview question for:
Role: {role}
Experience: {experience}
Interview Type: {interview_type}

Candidate Resume Context:
{resume_context}

Rules:
- Ask only one question
- Question MUST be based on candidate's resume/projects/skills
- Keep it relevant
- Difficulty should match experience
- No explanation
- Return only question
"""
    else:
        prompt = f"""
You are an expert technical interviewer.

Generate one interview question for:
Role: {role}
Experience: {experience}
Interview Type: {interview_type}

Rules:
- Ask only one question
- Ask a generic interview question related to the role
- Keep it relevant
- Difficulty should match experience
- No explanation
- Return only question
"""

    response = llm.invoke(prompt)

    state["current_question"] = response.content
    state["messages"].append(response.content)
    state["question_count"] += 1

    return state