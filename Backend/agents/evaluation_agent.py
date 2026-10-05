from Backend.llm import llm
import json


def evaluation_agent(state):
    print("Evaluation Agent Running...")

    question = state["current_question"]
    answer = state["user_answer"]

    prompt = f"""
You are an expert software engineering interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate based only on TEXT answer.

Score on:
1. Technical Knowledge (0-10)
2. Clarity of Explanation (0-10)
3. Problem Solving (0-10)

Return ONLY raw JSON.
Do NOT use markdown.
Do NOT add explanation.

Format:
{{
  "technical_score": 0,
  "clarity_score": 0,
  "problem_solving_score": 0,
  "strength": "",
  "weakness": ""
}}
"""

    response = llm.invoke(prompt)

    try:
        print(response.content)

        cleaned_response = response.content.strip()
        cleaned_response = cleaned_response.replace("```json", "")
        cleaned_response = cleaned_response.replace("```", "")

        result = json.loads(cleaned_response)

    except Exception as e:
        print("JSON Parsing Error:", e)

        result = {
            "technical_score": 5,
            "clarity_score": 5,
            "problem_solving_score": 5,
            "strength": "Average answer",
            "weakness": "Needs improvement"
        }

    state["evaluation"] = result
    return state