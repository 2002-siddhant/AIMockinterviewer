from langgraph.graph import StateGraph, END
from Backend.graph.state import InterviewState
from Backend.agents.interview_manager import interview_manager
from Backend.agents.question_generator import question_generator
from Backend.agents.evaluation_agent import evaluation_agent
from Backend.agents.feedback_agent import feedback_agent


def route_interview(state):
    if state["interview_complete"]:
        return "feedback_agent"
    return "question_generator"


builder = StateGraph(InterviewState)

builder.add_node("evaluation_agent", evaluation_agent)
builder.add_node("interview_manager", interview_manager)
builder.add_node("question_generator", question_generator)
builder.add_node("feedback_agent", feedback_agent)

builder.set_entry_point("evaluation_agent")

builder.add_edge("evaluation_agent", "interview_manager")

builder.add_conditional_edges(
    "interview_manager",
    route_interview
)

builder.add_edge("question_generator", END)
builder.add_edge("feedback_agent", END)

submit_graph = builder.compile()