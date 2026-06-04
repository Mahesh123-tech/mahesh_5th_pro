import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration parameters
st.set_page_config(
    page_title="Open-Text GK Quiz Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling classes
st.markdown("""
<style>
    .quiz-container {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .fact-card {
        background-color: #f0fdfa;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #0d9488;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .fact-title {
        font-weight: bold;
        color: #0d9488;
        font-size: 16px;
        margin-bottom: 5px;
    }
    .insight-card {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Question Bank equipped with multiple accepted textual variations to handle user phrasing inputs smoothly
QUIZ_BANK = [
    {
        "id": 1,
        "category": "Astronomy",
        "question": "Which planet in our solar system is known as the Red Planet?",
        "accepted_answers": ["mars"],
        "display_correct": "Mars",
        "fact": "Mars looks red because its surface material contains a high concentration of iron oxide (rust)."
    },
    {
        "id": 2,
        "category": "Geography",
        "question": "What is the longest river in the world?",
        "accepted_answers": ["nile", "nile river"],
        "display_correct": "Nile River",
        "fact": "The Nile River stretches roughly 6,650 kilometers (4,132 miles) and flows northward through northeastern Africa."
    },
    {
        "id": 3,
        "category": "Science",
        "question": "What is the hardest natural substance known on Earth?",
        "accepted_answers": ["diamond", "diamonds"],
        "display_correct": "Diamond",
        "fact": "Diamonds are made of pure carbon atoms tightly packed in a crystal lattice, giving them supreme structural hardness."
    },
    {
        "id": 4,
        "category": "History",
        "question": "Who was the first President of the United States?",
        "accepted_answers": ["george washington", "washington", "george washington "],
        "display_correct": "George Washington",
        "fact": "George Washington served from 1789 to 1797 and helped shape the democratic constitutional foundations of the nation."
    },
    {
        "id": 5,
        "category": "Oceanography",
        "question": "Which ocean is the largest and deepest on Earth?",
        "accepted_answers": ["pacific", "pacific ocean"],
        "display_correct": "Pacific Ocean",
        "fact": "The Pacific Ocean covers over 30% of the Earth's surface, spanning more area than all the world's continents combined."
    }
]

# --- SESSION STATE TRACKING INFRASTRUCTURE ---
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "is_answered" not in st.session_state:
    st.session_state.is_answered = False
if "submitted_answer" not in st.session_state:
    st.session_state.submitted_answer = ""

total_questions = len(QUIZ_BANK)

# --- SIDEBAR PRESENTATION & CONFIGURATION CONTROLS ---
st.sidebar.markdown("### 🏆 Live Quiz Progression")
progress_ratio = min(1.0, (st.session_state.current_index) / total_questions)
st.sidebar.progress(progress_ratio)

st.sidebar.markdown(f"**Progress Track:** Question {min(total_questions, st.session_state.current_index + 1)} of {total_questions}")
st.sidebar.markdown(f"**Live Points Score:** `{st.session_state.score}` / {total_questions}")

def clear_and_restart():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.is_answered = False
    st.session_state.submitted_answer = ""

if st.sidebar.button("🔄 Reset Quiz Profile"):
    clear_and_restart()
    st.rerun()

# --- MAIN ENGINE HEADER BLOCK ---
st.title("🧠 Open-TextInput GK Quiz & Deep Metrics Portal")
st.write("Type your answers into the blank interface window sequentially. The diagnostic engine flags errors, logs precision values, and generates charts.")
st.markdown("---")

# Conditional Routing: Terminal Assessment Complete Screen
if st.session_state.current_index >= total_questions:
    st.success("🎉 **All modules completed! Review your Terminal Diagnostics Summary Dashboard below.**")
    
    # 1. Core Summary Metrics Card Rows
    kpi1, kpi2, kpi3 = st.columns(3)
    final_score = st.session_state.score
    accuracy = (final_score / total_questions) * 100
    
    kpi1.metric("Total Correct Entries", f"{final_score} / {total_questions}")
    kpi2.metric("Accuracy Percentage", f"{accuracy:.1f}%")
    kpi3.metric("Assigned Rank Status", "Elite Scholar Master" if accuracy >= 80 else "Practicing Academicist")
    
    # 2. Performance Visualization Bar Plot Chart
    st.markdown("### 📈 Response
