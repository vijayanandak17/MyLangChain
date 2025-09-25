import streamlit as st
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.sidebar.warning("⚠️ OpenAI API key not found in .env.")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if not openai_api_key:
        st.info("Please provide an OpenAI API key to use this app.")
        st.stop()

# Create OpenAI client
client = OpenAI(api_key=openai_api_key)


def generate_email_with_openai(bullet_points: List[str], tone: str = "Professional") -> str:
    """
    Uses OpenAI GPT to generate a professional email from bullet points.
    """
    if not bullet_points:
        return ""

    bullets_text = "\n".join([f"- {point}" for point in bullet_points if point.strip()])

    system_prompt = (
        "You are a professional business communication assistant. "
        "Your task is to convert user-provided bullet points into a polished, formal email draft. "
        "Use a professional tone, proper email structure (greeting, body, closing), and clear language. "
        "Do not add any information not implied by the bullets. "
        "Address the recipient as '[Recipient's Name]' and sign off as '[Your Name]'."
    )

    user_prompt = (
        f"Write a {tone.lower()} business email based strictly on these bullet points:\n\n{bullets_text}\n\n"
        "Output only the email draft—no additional commentary or labels."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating email: {str(e)}")
        return ""


def main():
    st.set_page_config(
        page_title="Professional Email Assistant",
        page_icon="✉️",
        layout="centered"
    )

    # Header
    st.title("✉️ Professional Email Assistant")
    st.markdown("Transform bullet points into polished business emails using AI")

    # Input section
    st.subheader("Enter your key points")
    st.caption("Provide details as bullet points (one per line). Be specific about context, purpose, and action items.")

    user_input = st.text_area(
        label="Bullet Points",
        height=200,
        placeholder=(
            "• Project deadline extended to June 30\n"
            "• Budget approval needed for marketing campaign\n"
            "• Attached: revised proposal v2\n"
            "• Request feedback by Thursday"
        ),
        label_visibility="collapsed"
    )

    # Tone selection
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("Tone:")
    with col2:
        tone = st.radio(
            label="Email Tone",
            options=["Professional", "Formal", "Concise"],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )

    # Generate button
    generate = st.button("Generate Professional Email", type="primary", use_container_width=True)

    # Output section
    if generate and user_input.strip():
        bullets = [line.strip("•- \n\t") for line in user_input.split("\n") if line.strip()]
        if not bullets:
            st.warning("No valid bullet points found. Please enter at least one point.")
            return

        with st.spinner("Generating professional email with AI..."):
            email_draft = generate_email_with_openai(bullets, tone)

        if email_draft:
            st.subheader("Generated Email Draft")
            st.text_area(
                label="Email Draft",
                value=email_draft,
                height=400,
                label_visibility="collapsed"
            )

            # Action buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download Draft",
                    data=email_draft,
                    file_name="professional_email_draft.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col2:
                st.button(
                    "📋 Copy to Clipboard",
                    on_click=lambda: st.write(""),
                    help="Select text manually and copy (browser security limits auto-copy)",
                    use_container_width=True
                )

    elif generate and not user_input.strip():
        st.warning("Please enter at least one bullet point.")

    # Footer
    st.markdown("---")
    st.caption("🔒 Your inputs are sent to OpenAI only to generate the email. No data is stored by this app.")


if __name__ == "__main__":
    main()
