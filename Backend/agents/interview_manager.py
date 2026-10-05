def interview_manager(state):
    print("Interview Manager Running...")

    if state["question_count"] >= 7:
        state["interview_complete"] = True
    else:
        state["interview_complete"] = False

    return state