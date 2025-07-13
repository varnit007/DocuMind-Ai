import streamlit as st
from groq import Groq

# Initialize Groq client with your API key from Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def summarize_text(text):
    prompt = f"""
    Summarize the following document content clearly and concisely in bullet points:

    {text}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    summary = response.choices[0].message.content.strip()
    return summary
