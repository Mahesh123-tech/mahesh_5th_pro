import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page config for a professional analytics feel
st.set_page_config(
    page_title="Sequential GK Evaluation Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium visual styling
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

# Question Bank covering multiple disciplines
QUIZ_BANK = [
    {
        "id": 1,
        "category": "Astronomy",
        "question": "Which planet in our solar system is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "correct": "Mars",
        "fact": "Mars looks red because its surface material contains a high concentration of iron oxide (rust)."
    },
    {
        "id": 2,
        "category": "Geography",
        "question": "What is the longest river in the world?",
        "options": ["Amazon River", "Nile River", "Yangtze River", "Mississippi River"],
        "correct": "Nile River",
        "fact": "The Nile River stretches roughly 6,650 kilometers (4,132 miles) and flows northward through northeastern Africa."
    },
    {
        "id": 3,
        "category": "Science",
        "question": "What is the hardest natural substance known on Earth?",
        "options": ["Gold", "Iron", "Diamond", "Quartz"],
        "correct": "Diamond",
        "fact": "Diamonds are made of pure carbon atoms tightly packed in a crystal lattice, giving them supreme hardness."
    },
    {
        "id": 4,
        "category": "History",
        "question": "Who was the first President of the United States?",
        "options": ["Thomas Jefferson", "Abraham Lincoln", "George Washington", "John Adams"],
        "correct": "George Washington",
        "fact": "George Washington served from 1789 to 1797 and helped shape the democratic foundations of the nation."
    },
    {
        "id": 5,
        "category": "Oceanography",
        "question": "Which ocean is the largest and deepest on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct": "Pacific Ocean",
        "fact": "The Pacific Ocean covers over 30% of the Earth's surface, spanning more area than all the world's continents combined."
    }
]

# --- SESSION STATE MANAGEMENT ---
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "is_answered" not in st.session_state:
    st.session_state.is_answered = False
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

total_questions = len(QUIZ_BANK)

# --- SIDEBAR PRESENTATION & RESET CONTROL ---
st.sidebar.markdown("### 🏆 Live Quiz Progression")
progress_ratio = min(1.0, (st.session_state.current_index) / total_questions)
st.sidebar.progress(progress_ratio)

st.sidebar.markdown(f"**Progress:** Question {min(total_questions, st.session_state.current_index + 1)} of {total_questions}")
st.sidebar.markdown(f"**Current Score:** `{st.session_state.score}` / {total_questions}")

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.is_answered = False
    st.session_state.selected_answer = None

if st.sidebar.button("🔄 Reset Quiz Engine"):
    restart_quiz()
    st.rerun()

# --- MAIN APP UI HEADER ---
st.title("🧠 One-by-One GK Assessment & Deep Analytics Portal")
st.write("Answer questions sequentially. The system validates each input instantly, provides corrections, and analyzes performance metrics.")
st.markdown("---")

# Check if the quiz is finished
if st.session_state.current_index >= total_questions:
    st.success("🎉 **All questions completed! Review your Deep Analytics Dashboard below.**")
    
    # 1. High-Level Summary Statistics Rows
    kpi1, kpi2, kpi3 = st.columns(3)
    final_score = st.session_state.score
    accuracy = (final_score / total_questions) * 100
    
    kpi1.metric("Total Points Earned", f"{final_score} / {total_questions}")
    kpi2.metric("Accuracy Footprint", f"{accuracy:.1f}%")
    kpi3.metric("Expert Profile", "Elite Generalist" if accuracy >= 80 else "Developing Scholar")
    
    # 2. Performance Visualization Bar Chart
    st.markdown("### 📈 Visual Response Metrics Chart")
    history_df = pd.DataFrame(st.session_state.history)
    correct_count = len(history_df[history_df["Status"] == "✅ Correct"])
    incorrect_count = len(history_df[history_df["Status"] == "❌ Incorrect"])
    
    fig_summary = go.Figure()
    fig_summary.add_trace(go.Bar(
        x=['Correct Submissions', 'Incorrect Choices'],
        y=[correct_count, incorrect_count],
        marker_color=['#0d9488', '#ef4444'],
        width=0.35
    ))
    fig_summary.update_layout(
        title={'text': "Distribution Ratio of Selected Answers", 'x': 0.5, 'xanchor': 'center'},
        yaxis_title="Question Count",
        template="plotly_white",
        height=400
    )
    st.plotly_chart(fig_summary, use_container_width=True)
    
    # 3. Itemized Performance Review Grid
    st.
