import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration parameters
st.set_page_config(
    page_title="Open-Text GK Quiz Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe version-agnostic rerun wrapper to eliminate any AttributeError crashes
def trigger_safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

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

# Fixed Question Bank with text variation arrays for robust user matching
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
        "fact": "George Washington served from 1789 to 1797 and helped shape the democratic foundations of the nation."
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
    trigger_safe_rerun()

# --- MAIN ENGINE HEADER BLOCK ---
st.title("🧠 Open-TextInput GK Quiz & Deep Metrics Portal")
st.write("Type your answers into the blank interface window sequentially. The diagnostic engine flags errors, logs precision values, and generates charts.")
st.markdown("---")

# Conditional Routing: Quiz Complete Dashboard View
if st.session_state.current_index >= total_questions:
    st.success("🎉 **All modules completed! Review your Diagnostics Summary Dashboard below.**")
    
    # 1. Core Summary Metrics Card Rows
    kpi1, kpi2, kpi3 = st.columns(3)
    final_score = st.session_state.score
    accuracy = (final_score / total_questions) * 100 if total_questions > 0 else 0
    
    kpi1.metric("Total Correct Entries", f"{final_score} / {total_questions}")
    kpi2.metric("Accuracy Percentage", f"{accuracy:.1f}%")
    kpi3.metric("Assigned Rank Status", "Elite Scholar Master" if accuracy >= 80 else "Practicing Academicist")
    
    # 2. Extract History Safely with fallback defaults to prevent KeyError bugs
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        correct_count = len(history_df[history_df["Status Verification"] == "✅ Correct"])
        incorrect_count = len(history_df[history_df["Status Verification"] == "❌ Incorrect"])
    else:
        history_df = pd.DataFrame(columns=["Question Index ID", "Subject Focus Category", "Your Input Logged", "Expected Core Value", "Status Verification"])
        correct_count = 0
        incorrect_count = 0
    
    # 3. Performance Visualization Bar Plot Chart
    st.markdown("### 📈 Response Distribution Metrics Chart")
    fig_summary = go.Figure()
    fig_summary.add_trace(go.Bar(
        x=['Valid Matches', 'Mismatched Inputs'],
        y=[correct_count, incorrect_count],
        marker_color=['#0d9488', '#ef4444'],
        width=0.35
    ))
    fig_summary.update_layout(
        title={'text': "Distribution Analysis of Submitted Text Strings", 'x': 0.5, 'xanchor': 'center'},
        yaxis_title="Question Quantities",
        template="plotly_white",
        height=380
    )
    st.plotly_chart(fig_summary, use_container_width=True)
    
    # 4. Comprehensive Performance Evaluation Matrix Table Grid
    st.markdown("### 📋 Verification String Audit Matrix Grid")
    st.table(history_df)
    
    # 5. Automated Contextual Insights Summarization
    st.markdown("### 💡 Automated Knowledge Strategy Insights")
    st.markdown(f"""
    <div class="insight-card">
        <ul>
            <li><b>Text Precision Tracking:</b> You maintained a precise validation weight of <b>{accuracy:.1f}%</b> under active free-text constraint parameters.</li>
            <li><b>Recall Assessment Index:</b> Typing open text metrics removes guess-biases present in multiple-choice interfaces, creating a higher retention weight.</li>
            <li><b>Next Step Directive:</b> Click the left panel <b>'Reset Quiz Profile'</b> button to wipe your state records clean and initialize a fresh input run.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    # Render Current Active Question State Layout Block
    current_question = QUIZ_BANK[st.session_state.current_index]
    
    st.markdown(f"### 🚀 Evaluating Subject Sector: `{current_question['category']}`")
    
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown(f"🧬 **Question {current_question['id']}:** {current_question['question']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Text input configuration with an explicit unique key for each question index
    user_typed_input = st.text_input(
        "Type your answer text below in the blank field box:",
        value="",
        placeholder="Type response sequence here...",
        disabled=st.session_state.is_answered,
        key=f"q_text_{st.session_state.current_index}"
    )
    
    st.markdown("---")
    
    # Validation step logic
    if not st.session_state.is_answered:
        if st.button("🎯 Verify & Validate My Typed Answer"):
            if user_typed_input.strip() == "":
                st.warning("⚠️ Text space is currently empty! Please fill in the answer input field first.")
            else:
                st.session_state.submitted_answer = user_typed_input
                st.session_state.is_answered = True
                trigger_safe_rerun()
                
    else:
        # Evaluate free-form inputs case-insensitively against valid variations
        final_answer_string = st.session_state.submitted_answer
        user_clean = final_answer_string.strip().lower()
        
        is_right = user_clean in current_question["accepted_answers"]
        target_display_answer = current_question["display_correct"]
        
        if is_right:
            st.success(f"✨ **Correct! Excellent Precision.** You correctly typed and matched: **{target_display_answer}**.")
        else:
            st.error(f"❌ **Incorrect Match Registered.** You entered: '{final_answer_string}'. The correct targeted option is **{target_display_answer}**.")
            
        # Display the contextual educational explanation snippet box
        st.markdown(f"""
        <div class="fact-card">
            <div class="fact-title">💡 Did You Know?</div>
            <p style="margin: 0; color: #0f766e; font-size: 15px;">{current_question['fact']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Advance button rendering logic
        button_label = "Proceed to Next Question ➡️" if (st.session_state.current_index + 1 < total_questions) else "Unlock Final Metrics Dashboard 📊"
        
        if st.button(button_label):
            # Append diagnostic parameter logs
            st.session_state.history.append({
                "Question Index ID": f"Q-{current_question['id']}",
                "Subject Focus Category": current_question["category"],
                "Your Input Logged": final_answer_string,
                "Expected Core Value": target_display_answer,
                "Status Verification": "✅ Correct" if is_right else "❌ Incorrect"
            })
            
            # Increment point indicator score
            if is_right:
                st.session_state.score += 1
                
            # Shift loop index pointers forward and clear step visibility flags
            st.session_state.current_index += 1
            st.session_state.is_answered = False
            st.session_state.submitted_answer = ""
            trigger_safe_rerun()
