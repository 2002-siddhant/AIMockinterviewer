import streamlit as st
import requests

st.set_page_config(page_title="AI Mock Interviewer", layout="wide")

st.title("Agentic AI Mock Interviewer")
st.markdown("Practice AI-powered placement interviews")

with st.sidebar:
    st.header("Interview Setup")

    role = st.selectbox("Role", ["SDE", "ML Engineer", "Data Scientist"])
    experience = st.selectbox("Experience", ["Fresher", "1-3 years", "3+ years"])
    interview_type = st.selectbox("Interview Type", ["Technical", "HR", "System Design"])

    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Start Interview"):

    payload = {
        "role": role,
        "experience": experience,
        "interview_type": interview_type
    }

    response = requests.post(
        "http://127.0.0.1:8000/create-session",
        json=payload
    )

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    data = response.json()
    session_id = data["session_id"]

    st.session_state.session_id = session_id

    if resume is not None:
        files = {
            "file": (resume.name, resume.getvalue(), "application/pdf")
        }

        upload_response = requests.post(
            f"http://127.0.0.1:8000/upload-resume?session_id={session_id}",
            files=files
        )

        if upload_response.status_code != 200:
            st.error(upload_response.text)
            st.stop()

    response = requests.post(
        "http://127.0.0.1:8000/start-interview",
        json={"session_id": session_id}
    )

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    data = response.json()
    st.session_state.question = data["question"]
    st.session_state.question_number = 1


if "question" in st.session_state:
    question_number = st.session_state.get("question_number", 1)

    st.subheader(f"Question {question_number}/3")

    progress = question_number / 3
    st.progress(progress)

    st.info(st.session_state.question)

if "session_id" in st.session_state:

    with st.form("answer_form"):
        answer = st.text_area("Your Answer")
        submitted = st.form_submit_button("Submit Answer")

    if submitted:
        payload = {
            "session_id": st.session_state.session_id,
            "answer": answer
        }

        response = requests.post(
            "http://127.0.0.1:8000/submit-answer",
            json=payload
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response.json()

        if data["interview_complete"]:
           st.success("Interview Completed!")

           st.subheader("Final Feedback")
           st.markdown(data["feedback"]) 
          


        else:
           st.session_state.question = data["next_question"]
           st.session_state.question_number += 1
           st.rerun()