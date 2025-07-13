import streamlit as st
from groq import Groq
import re

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_questions(context, num_questions=3):
    prompt = f"""
    Based on the following document content, generate {num_questions} multiple-choice questions that test comprehension or logical understanding.

    Format:
    Q: Question here?
    Options: ["Option1", "Option2", "Option3", "Option4"]
    A: Correct Answer

    Document:
    {context}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response.choices[0].message.content.strip()
    return parse_questions(raw_output)

def parse_questions(text):
    questions = []
    pattern = r"Q:\s*(.*?)\nOptions:\s*\[(.*?)\]\nA:\s*(.*)"
    matches = re.finditer(pattern, text, re.DOTALL)
    for match in matches:
        question = match.group(1).strip()
        options = [opt.strip().strip('"') for opt in match.group(2).split(",")]
        answer = match.group(3).strip().strip('"')
        questions.append({
            "q": question,
            "options": options,
            "a": answer
        })
    return questions

def evaluate_answer(user_answer, correct_answer):
    user = user_answer.lower().strip()
    correct = correct_answer.lower().strip()
    if correct in user or user in correct:
        return True, "✅ Well done! Your answer seems correct."
    else:
        return False, f"❌ Expected something like: {correct_answer}"
