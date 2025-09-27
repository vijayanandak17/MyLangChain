import streamlit as st
import random
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Load API Key (you can also set it in .env or Streamlit secrets)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

st.title("🎯 Mock Interview Simulator")

# Step 1: Get Role and JD
role = st.text_input("Enter the Role (e.g., Python Developer, Data Scientist):")
job_desc = st.text_area("Paste the Job Description here:")

# Session state for interview flow
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "scores" not in st.session_state:
    st.session_state.scores = []
if "responses" not in st.session_state:
    st.session_state.responses = []

# Function to generate 3 interview questions
def generate_questions(role, jd):
    prompt = f"""
    You are an expert technical interviewer. 
    Generate 5 short, focused technical interview questions for the role of {role}.
    Use this job description as context:
    {jd}
    Provide the questions as a plain list, no explanations.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are an expert interviewer."},
                  {"role":"user","content":prompt}]
    )
    all_qs = response.choices[0].message.content.strip().split("\n")
    # Clean and pick any 3 randomly
    questions = [q.strip("- ").strip() for q in all_qs if q.strip()]
    return random.sample(questions, 3) if len(questions) >= 3 else questions

# Function to validate candidate response (Corrective RAG style scoring)
def validate_answer(role, jd, question, answer):
    prompt = f"""
    You are evaluating a candidate's response in a mock interview.
    Role: {role}
    Job Description: {jd}

    Question: {question}
    Candidate Answer: {answer}

    Task:
    1. Analyze correctness, depth, and relevance.
    2. Give a percentage score (0–100).
    3. Provide brief feedback.

    Respond strictly in JSON:
    {{
        "score": <number>,
        "feedback": "<short feedback>"
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are an expert interviewer and evaluator."},
                  {"role":"user","content":prompt}]
    )
    import json
    try:
        result = json.loads(response.choices[0].message.content)
        return result.get("score", 0), result.get("feedback", "No feedback")
    except:
        return 0, "Error parsing evaluation."

# Start Interview Button
if st.button("Start Interview") and role and job_desc:
    st.session_state.questions = generate_questions(role, job_desc)
    st.session_state.current_q = 0
    st.session_state.scores = []
    st.session_state.responses = []
    st.success("✅ Interview Started! Answer the questions one by one.")

# Interview Q&A Flow
if st.session_state.questions and st.session_state.current_q < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current_q]
    st.subheader(f"Question {st.session_state.current_q+1}: {q}")

    user_answer = st.text_area("Your Answer:", key=f"answer_{st.session_state.current_q}")

    if st.button("Submit Answer"):
        if user_answer.strip():
            score, feedback = validate_answer(role, job_desc, q, user_answer)
            st.session_state.scores.append(score)
            st.session_state.responses.append(user_answer)
            st.info(f"💡 Feedback: {feedback}")
            st.success(f"Score: {score}%")
            st.session_state.current_q += 1
        else:
            st.warning("⚠️ Please enter an answer before submitting.")

# Final Result
if st.session_state.questions and st.session_state.current_q >= len(st.session_state.questions):
    avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
    st.subheader("📊 Final Result")
    st.write(f"Average Score: **{avg_score:.2f}%**")

    if avg_score >= 60:
        st.success("🎉 Congratulations! Candidate is SELECTED for the job.")
    else:
        st.error("🙏 Better luck next time.")
