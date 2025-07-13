import streamlit as st
import time
from groq import Groq
from backend.file_loader import load_document
from backend.challenge import generate_questions, evaluate_answer

# ---------------------- PAGE CONFIG ---------------------- #
st.set_page_config(page_title="DocuMind AI", layout="centered")

# ---------------------- SESSION STATE INIT ---------------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
    
# ---------------------- SUMMARIZER FUNCTION ---------------------- #
def summarize_text(text):
    prompt = f"""
You are a helpful assistant. Summarize the following document into clear, concise bullet points. Focus on the key concepts, facts, or logic.

Document:
{text[:3000]}
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert summarizer. Provide bullet points only."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# ---------------------- GROQ CLIENT ---------------------- #
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------- HERO SECTION ---------------------- #
st.markdown("""
    <div style="background: linear-gradient(90deg, #4f46e5, #ec4899);
                padding: 3rem 1rem; text-align: center;
                border-radius: 0 0 20px 20px; color: white;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1); position: relative;">
        <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 0.5rem;
                   background: -webkit-linear-gradient(45deg, #3b82f6, #ec4899);
                   -webkit-background-clip: text; -webkit-text-fill-color: white;">
            Transform Documents<br>Into Intelligence
        </h1>
        <p style="font-size: 1.25rem; max-width: 700px; margin: auto; color: #f3f4f6;">
            Upload any document and unlock instant insights, intelligent Q&A, and personalized challenges powered by advanced AI technology.
        </p>
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712037.png" style="position: absolute; top: 20px; left: 20px; width: 60px;">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" style="position: absolute; top: 20px; right: 20px; width: 60px;">
    </div>
""", unsafe_allow_html=True)

# ---------------------- FILE UPLOAD ---------------------- #
st.markdown("### 📁 Upload Folder or File")
uploaded_file = st.file_uploader("Choose your document", label_visibility="collapsed")
if uploaded_file is not None:
    st.session_state.document_text = load_document(uploaded_file)
    file_size_kb = round(len(uploaded_file.getvalue()) / 1024, 2)
    file_name = uploaded_file.name

    with st.container():
        st.markdown(f"""
            <div style='background: linear-gradient(145deg, #1a1a2e, #0f0f1a);
                        border-radius: 20px; padding: 30px; color: white;
                        box-shadow: 0 0 20px rgba(0,255,255,0.3); text-align: center;'>
                <div style='font-size: 48px;'>📁</div>
                <h3>{file_name}</h3>
                <p>{file_size_kb} KB</p>
            </div>
        """, unsafe_allow_html=True)

        progress = st.progress(0)
        status = st.empty()
        for i in range(101):
            time.sleep(0.005)
            progress.progress(i)
            status.markdown(f"*Uploading... {i}%*")
        status.markdown("✅ *Upload Complete!*")

    # ---------------------- AUTO SUMMARY ---------------------- #
    with st.spinner("Summarizing document..."):
        st.session_state.summary = summarize_text(st.session_state.document_text)

    st.markdown("### 📝 Document Summary")
    st.markdown(f"""
        <div style='background: #f0f0ff; padding: 20px;
                    border-radius: 16px; box-shadow: 0 0 15px rgba(0,0,0,0.05);'>
            {st.session_state.summary.replace('-', '•')}
        </div>
    """, unsafe_allow_html=True)

# ---------------------- TABS ---------------------- #
st.markdown("""
<style>
.custom-tab {
    display: flex; justify-content: space-evenly; margin-bottom: 1rem;
}
.tab-box {
    width: 200px; background-color: #f1f3f6; border-radius: 16px;
    text-align: center; padding: 20px 10px; cursor: pointer;
    box-shadow: 0 0 6px rgba(0,0,0,0.1); transition: 0.2s;
}
.tab-box:hover {
    transform: scale(1.02); box-shadow: 0 0 10px rgba(98,0,234,0.4);
}
.active-tab {
    background-color: white; border: 2px solid #6200ea;
}
</style>
""", unsafe_allow_html=True)

selected_tab = st.radio("Select Tab", ["Ask Anything", "Challenge Me", "Info"], horizontal=True, label_visibility="collapsed")

# ---------------------- ASK ANYTHING ---------------------- #
if selected_tab == "Ask Anything":
    st.markdown("<div class='custom-tab'><div class='tab-box active-tab'><img src='https://cdn-icons-png.flaticon.com/512/2645/2645998.png' width='50'/><br><strong>Ask Anything</strong></div></div>", unsafe_allow_html=True)
    st.markdown("#### 🤖 Ask our Assistant Anything")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

    user_input = st.chat_input("Ask a question")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": f"You are an AI assistant. Here is the document content:\n\n{st.session_state.document_text[:3000]}"},
                    *st.session_state.messages
                ]
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})


    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

# ---------------------- CHALLENGE ME ---------------------- #
elif selected_tab == "Challenge Me":
    st.markdown("<div class='custom-tab'><div class='tab-box active-tab'><img src='https://cdn-icons-png.flaticon.com/512/8581/8581104.png' width='50'/><br><strong>Challenge Me</strong></div></div>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Let's Test Your Brain")

    if not st.session_state.document_text:
        st.warning("Please upload a document first.")
        st.stop()

    if not st.session_state.quiz_data:
        with st.spinner("Generating quiz from document..."):
            st.session_state.quiz_data = generate_questions(st.session_state.document_text)

    quiz_data = st.session_state.quiz_data
    step = st.session_state.quiz_step

    if step < len(quiz_data):
        question = quiz_data[step]
        st.write(f"*Q{step+1}: {question['q']}*")
        choice = st.radio("", question["options"], key=f"q{step}")
        if st.button("Submit", key=f"submit{step}"):
            is_correct, feedback = evaluate_answer(choice, question["a"])
            st.info(feedback)
            if is_correct:
                st.session_state.score += 1
            st.session_state.quiz_step += 1
    else:
        st.success(f"✅ Quiz complete! Your score: {st.session_state.score}/{len(quiz_data)}")
        if st.button("Restart Quiz"):
            st.session_state.quiz_step = 0
            st.session_state.score = 0
            st.session_state.quiz_data = []

# ---------------------- INFO ---------------------- #
else:
    st.markdown("<div class='custom-tab'><div class='tab-box active-tab'><img src='https://cdn-icons-png.flaticon.com/512/1250/1250614.png' width='50'/><br><strong>Info</strong></div></div>", unsafe_allow_html=True)
    st.markdown("DocuMind AI is your intelligent document assistant powered by LLaMA 3 and Streamlit.")
    st.markdown("- 📥 Upload PDF/TXT files\n- 🤖 Ask questions via LLM\n- 🎯 Generate and solve document-based quizzes")

# ---------------------- FOOTER ---------------------- #
st.markdown("---")
