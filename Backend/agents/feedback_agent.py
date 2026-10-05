from Backend.llm import llm


def feedback_agent(state):
    print("Feedback Agent Running...")

    question = state["current_question"]
    answer = state["user_answer"]
    evaluation = state["evaluation"]

    prompt = f"""
You are an expert software engineering interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluation:
{evaluation}

Generate personalized interview feedback.

Rules:
- Feedback must be specific to candidate answer
- Avoid generic feedback
- Keep concise and actionable

Format:

Strengths:
- ...

Weaknesses:
- ...

Suggestions:
- ...
"""

    response = llm.invoke(prompt)

    state["feedback"] = response.content
    return state