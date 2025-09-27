import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- Initialize OpenAI client ---
client = OpenAI(api_key=api_key)

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Cover Letter Generator", page_icon="✍️", layout="centered")
st.title("✍️ AI-Powered Cover Letter Generator")
st.markdown("Generate a tailored cover letter in seconds by entering a few details.")

# --- User Inputs ---
role = st.text_input("Role you are applying for", placeholder="e.g., Data Analyst")
company = st.text_input("Company name", placeholder="e.g., Microsoft")
experience = st.selectbox(
    "Your experience level",
    ["Entry-level", "Mid-level", "Senior-level", "Executive"],
    index=0
)

generate_button = st.button("Generate Cover Letter")

# --- Generate Cover Letter ---
if generate_button:
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please add it to your .env file.")
    elif not role or not company:
        st.warning("Please fill in both the role and company name.")
    else:
        with st.spinner("Crafting your personalized cover letter..."):
            prompt = f"""
            Write a professional cover letter for a {experience} professional 
            applying for the role of {role} at {company}.
            Make it concise, tailored, and compelling.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",  # Use "gpt-3.5-turbo" if "gpt-4o" isn't available to you
                    messages=[
                        {"role": "system", "content": "You are a career coach helping write professional cover letters."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400,
                    temperature=0.7
                )

                cover_letter = response.choices[0].message.content.strip()

                # --- Display Output ---
                st.subheader("📄 Your Tailored Cover Letter")
                st.write(cover_letter)

                # --- Download Option ---
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")
