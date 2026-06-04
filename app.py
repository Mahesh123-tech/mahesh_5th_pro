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
    st.markdown("### 📋 Response Audit Grid Matrix")
    st.table(history_df)
    
    # 4. Contextual Automation Insights
    st.markdown("### 💡 Strategy and Context Insights")
    st.markdown(f"""
    <div class="insight-card">
        <ul>
            <li><b>Performance Footprint:</b> Your accuracy rating reached <b>{accuracy:.1f}%</b> under sequential evaluation rules.</li>
            <li><b>Behavioral Matrix:</b> Real-time correction prevents memory gaps, cementing new facts right after a misstep.</li>
            <li><b>Next Step Guide:</b> Use the left sidebar reset button if you want to wipe parameters and retry for a 100% perfect score.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    # Render Active Question Form
    current_question = QUIZ_BANK[st.session_state.current_index]
    
    st.markdown(f"### 🚀 Evaluating Subject Layer: `{current_question['category']}`")
    
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown(f"🧬 **Question {current_question['id']}:** {current_question['question']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Render radio selections. Disable input if already answered to prevent retroactively changing answers.
    chosen_radio = st.radio(
        "Select your strategic choice alternative:",
        options=current_question["options"],
        disabled=st.session_state.is_answered,
        key=f"q_radio_{st.session_state.current_index}"
    )
    
    # Evaluation Action Buttons
    if not st.session_state.is_answered:
        if st.button("🎯 Lock and Validate Answer"):
            st.session_state.selected_answer = chosen_radio
            st.session_state.is_answered = True
            st.rerun()
            
    else:
        # Step 2: Answer is locked in. Evaluate correctness and provide immediate response/correction feedback.
        user_ans = st.session_state.selected_answer
        correct_ans = current_question["correct"]
        is_right = (user_ans == correct_ans)
        
        if is_right:
            st.success(f"✨ **Correct!** Excellent pick. You successfully chose **{correct_ans}**.")
        else:
            st.error(f"❌ **Incorrect Choice Locked In.** You answered **{user_ans}**. The correct target answer is **{correct_ans}**.")
            
        # Display the explanatory information block regardless
        st.markdown(f"""
        <div class="fact-card">
            <div class="fact-title">💡 Did You Know? (Educational Fact)</div>
            <p style="margin: 0; color: #0f766e; font-size: 15px;">{current_question['fact']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation element to advance forward sequentially
        button_text = "Proceed to Next Question ➡️" if (st.session_state.current_index + 1 < total_questions) else "Unlock Final Analytics Dashboard 📊"
        
        if st.button(button_text):
            # Record choice parameters into historical tracking array before resetting question context
            st.session_state.history.append({
                "ID": f"Q-{current_question['id']}",
                "Category": current_question["category"],
                "Your Input": user_ans,
                "Correct Option": correct_ans,
                "Status": "✅ Correct" if is_right else "❌ Incorrect"
            })
            
            # Increment score if applicable
            if is_right:
                st.session_state.score += 1
                
            # Move index forward and clear validation state locks
            st.session_state.current_index += 1
            st.session_state.is_answered = False
            st.session_state.selected_answer = None
            st.rerun()
