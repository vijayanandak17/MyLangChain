import streamlit as st
import os
from dotenv import load_dotenv
import openai

# Load API key from .env
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")  # openai-python v1.x does NOT use api_key this way

# Create OpenAI client
client = openai.OpenAI()  # Uses OPENAI_API_KEY from .env automatically

st.set_page_config(
    page_title="Python Coding Assistant",
    page_icon=":snake:",
    layout="centered"
)

st.markdown(
    """
    <style>
        .stTextInput [data-baseweb="input"] {font-size: 18px;}
        .stTextArea textarea {font-size: 16px;}
        .stButton button {font-size: 18px; background-color: #0099ff; color: #fff; border-radius: 8px;}
        .st-cq {background-color: #f7f7f9;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🐍 Python Coding Assistant")
st.caption("Get Python code help and explanations with OpenAI GPT")

user_code = st.text_area(
    "Enter your Python code or describe your coding problem:",
    height=200,
    placeholder="Type your code or question here..."
)

coding_goal = st.text_input(
    "Optional: What do you want to achieve?",
    placeholder="e.g., optimize this function, fix the bug..."
)

if st.button("Ask Assistant"):
    if not user_code.strip():
        st.warning("Please enter a code snippet or question.")
    else:
        st.info("Asking the assistant...")

        base_prompt = (
            "You are a helpful Python coding assistant. "
            "Explain and, if needed, improve, fix, or annotate the code or answer the user's question clearly. "
            "Respond with readable Python code blocks for code, and clear answers for explanations.\n\n"
        )

        prompt = base_prompt + f"User's input:\n{user_code}\n"
        if coding_goal.strip():
            prompt += f"\nGoal: {coding_goal}\n"

        try:
            # Use the latest OpenAI API structure
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if available to you
                messages=[
                    {"role": "system", "content": base_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=900,
                temperature=0.2,
            )
            output = response.choices[0].message.content
            st.markdown("**Assistant's Response:**")
            st.markdown(output)
        except Exception as e:
            st.error(f"Error contacting OpenAI API: {e}")

st.markdown(
    """
    ---
    **Your API key is kept secure in a `.env` file.**
    """,
    unsafe_allow_html=True,
)
