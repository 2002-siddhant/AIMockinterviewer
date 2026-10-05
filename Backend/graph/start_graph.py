from langgraph.graph import StateGraph, END
from Backend.graph.state import InterviewState
from Backend.agents.interview_manager import interview_manager
from Backend.agents.question_generator import question_generator

builder = StateGraph(InterviewState)

builder.add_node("interview_manager", interview_manager)
builder.add_node("question_generator", question_generator)

builder.set_entry_point("interview_manager")

builder.add_edge("interview_manager", "question_generator")
builder.add_edge("question_generator", END)

start_graph = builder.compile()