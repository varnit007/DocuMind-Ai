# 🧠 DocuMind AI

 DocuMind AI is your intelligent document companion — upload any file, chat with an AI assistant, and challenge your knowledge with smart quizzes. Built with Streamlit + Gorq AI for seamless interaction and real-time insights.
DocuMind AI** is a smart document assistant built with **Streamlit** and powered by **Groq API**. Upload any document, ask intelligent questions using blazing-fast LLMs, and challenge yourself with interactive quizzes — all in one beautiful, AI-powered app.

![Hero](https://plagiarismdetector.net/tool-imges/al-powered-summerizer.svg)

---

## 🚀 Features

- 📁 **Animated File Upload**  
  Upload documents with smooth progress visualization and modern UI effects.

- 💬 **Ask Anything**  
  Chat with the Groq-powered LLaMA 3 model to ask contextual questions or general queries.

- 🎯 **Challenge Me**  
  Take interactive quizzes to test your memory and understanding — AI doesn’t just answer, it challenges you too.

- 🎨 **Modern Interface**  
  Includes gradient hero sections, custom icons, dark/light card styling, and animated buttons.

- 🧾 **Session Memory**  
  Chat history and quiz scores are preserved during each app session using `st.session_state`.

- 🔐 **Secure API Handling**  
  Your Groq API key is stored securely using Streamlit's secret manager.

---

## ⚙️ Tech Stack

| Layer     | Technology            |
|-----------|------------------------|
| 💻 Frontend | [Streamlit](https://streamlit.io) |
| 🧠 AI Engine | [Groq API](https://console.groq.com) – LLaMA 3 / Mixtral |
| 🎨 Icons    | [Flaticon](https://flaticon.com) |
| 💬 Language | Python + Markdown UI |

---

## ⚙ Setup Instructions

### 1. Clone the Repository

bash
git clone https://github.com/your-username/genai-research-assistant.git
cd genai-research-assistant


### 2. Create and Activate Virtual Environment

bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# OR Activate on macOS/Linux
source venv/bin/activate


### 3. Install Dependencies

bash
pip install -r requirements.txt


### 4. Run the Streamlit App

bash
streamlit run app.py
# 🧠 DocuMind AI – Architecture Guide

DocuMind AI is a modular, front-end-first productivity assistant powered by **Streamlit** and **Groq's blazing-fast LLM API**. It allows users to upload documents, chat with AI, and take intelligent quizzes in a beautiful interface.

graph TD
    A[👤 User Launches App] --> B{Select Action}
    
    B --> C1[📁 Upload Document]
    C1 --> D1[📊 Show Animated Progress]
    D1 --> E1[✅ Confirm Upload]
    
    B --> C2[💬 Ask Anything]
    C2 --> D2[🔁 Send Message to Groq API]
    D2 --> E2[🧠 Get AI Response (LLaMA 3)]
    E2 --> F2[💬 Display in Chat Bubble]

    B --> C3[🎯 Challenge Me (Quiz)]
    C3 --> D3[📋 Display MCQ]
    D3 --> E3{Submit Answer}
    E3 --> F3[✔️ Evaluate & Track Score]
    
    F2 --> G[User Asks Next Question]
    F3 --> H[Next Question or Show Final Score]

