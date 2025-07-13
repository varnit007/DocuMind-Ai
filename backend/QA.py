import streamlit as st
from groq import Groq

# Initialize Groq client with your API key from Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def answer_question(context, question):
    prompt = f"""
    Based on the following context, answer the question accurately.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content.strip()
    return answer
