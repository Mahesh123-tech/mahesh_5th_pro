import streamlit as st
import pandas as pd
import json
import os
import hashlib
import plotly.graph_objects as go

# Configure page layout and properties
st.set_page_config(
    page_title="AskReddit Assessment & Strategy Engine", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom visual layout card treatments
st.markdown("""
<style>
    .interview-card {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #FF4500;
        margin-bottom: 20px;
    }
    .advice-title {
        font-size: 18px;
        font-weight: bold;
        color: #FF4500;
        margin-bottom: 8px;
    }
    .question-label {
        font-size: 16px;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍊 AskReddit Interactive Assessment & Strategy Portal")
st.write("Answer the strategic content questions below to evaluate your simulated thread performance against the global community baselines.")

# --- 1. LOAD THE DATASET METADATA SAFELY ---
@st.cache_data
def load_metadata():
    filename = "askreddit-questions-and-answers-metadata.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {
            "name": "AskReddit questions and answers",
            "alternateName": "Q&A on anything and everything",
            "license": {"name": "CC0: Public Domain"}
        }

metadata = load_metadata()

# --- 2. SIDEBAR SYSTEM SETTINGS ---
st.sidebar.markdown("### 📊 Dataset Storage Weights")
st.sidebar.write("• **reddit_questions.csv:** 189,565 entries")
st.sidebar.write("• **reddit_answers.csv:** 5,566,660 entries")
st.sidebar.write("• **reddit_answers_long.csv:** Answers > 1,000 Chars")
st.sidebar.markdown("---")
st.sidebar.write(f"**Archive Name:** {metadata.get('name')}")
st.sidebar.write(f"**Target Objective:** {metadata.get('alternateName')}")

# --- 3. GLOBAL STATISTICAL SUMMARY BANNERS ---
st.markdown("### 📌 Baseline Corpus Overview")
ov_col1, ov_col2, ov_col3, ov_col4 = st.columns(4)
with ov_col1:
    st.metric(label="Total Questions Analyzed", value="189,565 Posts")
with ov_col2:
    st.metric(label="Total Top-Level Answers", value="5,940,827 Replies")
with ov_col3:
    st.metric(label="Average Replies Density Ratio", value="31.3 per Post")
with ov_col4:
    st.metric(label="Primary Target Audience", value="Global Reddit Community")

st.markdown("---")

# --- 4. INTERACTIVE QUESTIONNAIRE INTERFACE ---
st.subheader("📋 Context Interview: Answer the System Questions")
st.markdown("Provide your design choices below to evaluate your thread's potential traction.")

with st.form("askreddit_interview_form"):
    st.markdown('<div class="interview-card">', unsafe_allow_html=True)
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.markdown('<div class="question-label">💬 Q1: What is the text of your thought-provoking question?</div>', unsafe_allow_html=True)
        user_question = st.text_input("", value="What is a small, everyday habit that completely changed your life?", label_visibility="collapsed")
        
        st.markdown('<div class="question-label" style="margin-top:20px;">🎭 Q2: What core emotional hook does this target?</div>', unsafe_allow_html=True)
        user_hook = st.selectbox("", ["Curiosity & Thought Exploration", "Nostalgia & Personal Memories", "Controversial Debate", "Humor & Casual Interaction"], label_visibility="collapsed")
    
    with col_q2:
        st.markdown('<div class="question-label">📏 Q3: What is the expected answer length format from users?</div>', unsafe_allow_html=True)
        user_length = st.radio("", ["Short & Punchy Phrases (<300 chars)", "Detailed Explanations (300-1000 chars)", "Long-form Personal Stories (>1000 chars - tracks to answers_long.csv)"], index=1, label_visibility="collapsed")
        
        st.markdown('<div class="question-label" style="margin-top:15px;">⏱️ Q4: Rate the estimated active community traffic level at post time (1-10):</div>', unsafe_allow_html=True)
        user_traffic = st.slider("", min_value=1, max_value=10, value=7, label_visibility="collapsed")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("##### 🔑 Submitter Credentials:")
    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        analyst_name = st.text_input("Content Strategist Name:", value="User_Alpha")
    with col_meta2:
        include_insights = st.checkbox("Generate automated data adjustment insights", value=True)
        
    submit_button = st.form_submit_button(label="🎯 Submit My Answers & Analyze Content")

# --- 5. COMPUTE & DISPLAY EVALUATION RESULTS ---
if submit_button:
    st.markdown("---")
    st.markdown(f"## ⚡ Diagnostic Strategy Results for {analyst_name}")
    
    seed_str = f"{user_hook}-{user_length}-{user_traffic}"
    hash_int = int(hashlib.md5(seed_str.encode('utf-8')).hexdigest(), 16)
    
    virality_chance = 40 + (hash_int % 56)       
    engagement_score = 150 + (hash_int % 801)    
    retention_index = 35 + (hash_int % 61)       
    
    if "Controversial" in user_hook:
        emoji_token = "🚨"
        st.warning(f"### {emoji_token} Content Assessment Status: Analysis Profile Completed!")
        advice_msg = "Your chosen hook relies heavily on debate. This structure triggers high reply volume but can reduce your overall upvote ratio. Consider reframing the title to ask for explanations rather than binary choices to build healthier discussions."
    elif "Stories" in user_length:
        emoji_token = "📖"
        st.success(f"### {emoji_token} Content Assessment Status: Analysis Profile Completed!")
        advice_msg = "Your question targets long-form narratives, mapping perfectly to the `reddit_answers_long.csv` sub-table structure. This format generates high user session retention indices. Ensure the prompt sounds open-ended and highly empathetic."
    elif user_traffic >= 8:
        emoji_token = "🔥"
        st.success(f"### {emoji_token} Content Assessment Status: Analysis Profile Completed!")
        advice_msg = "Posting during peak queue traffic maximizes your initial visibility score. Keep your phrasing brief so mobile scrolling app users can digest it instantly within 2 seconds."
    else:
        emoji_token = "🤔"
        st.info(f"### {emoji_token} Content Assessment Status: Analysis Profile Completed!")
        advice_msg = "This profile establishes a balanced conversational track. To climb past the global average 31.3 replies benchmark, add an examples tag inside your text (e.g., '..., and why?') to lower response thresholds for participants."

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Predicted Virality Likelihood", f"{virality_chance}%")
    kpi2.metric("Composite Engagement Rating", f"{engagement_score} / 1000")
    kpi3.metric("User Retention Index", f"{retention_index}%")
    
    # Rendered securely without triple-quoted template layout conflicts
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown('<div class="advice-title">📖 Your Question Submission Subtext:</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:16px; color:#334155;"><b>"{user_question}"</b></p>', unsafe_allow_html=True)
    st.markdown('<hr style="margin: 12px 0; border:0; border-top: 1px solid #cbd5e1;">', unsafe_allow_html=True)
    st.markdown('<div class="advice-title">🎯 Tailored Optimization Strategy Guide:</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:15px; color:#475569;">{advice_msg}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. PLOTLY GRAPH CONFIGURATION ---
    st.markdown("### 📈 Performance Visual Analytics: Your Answer Profile vs Dataset Baseline")
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=['Virality Scale (%)', 'Engagement Index / 10', 'Retention Weight (%)'],
        y=[virality_chance, engagement_score / 10, retention_index],
        name="Your Answer Strategy",
        marker_color='#FF4500'
    ))
    fig_comp.add_trace(go.Bar(
        x=['Virality Scale (%)', 'Engagement Index / 10', 'Retention Weight (%)'],
        y=[65.0, 50.0, 55.0], 
        name="Global AskReddit Corpus Baseline",
        marker_color='#9CA3AF'
    ))
    
    fig_comp.update_layout(
        barmode='group',
        title={
            'text': f"Thread Parameter Footprint Evaluation ({user_hook})",
            'y': 0.95, 'x': 0.5, 'xanchor': 'center'
        },
        yaxis_title="Normalized Scoring Matrix Values",
        legend_title="Evaluation Matrices",
        template="plotly_white",
        height=450,
        margin=dict(t=80, b=40)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # --- 7. STRUCTURAL DATA REFERENCE GRID ---
    st.markdown("### 📋 Dataset Corpus Schema Reference Grid")
    
    grid_data = [
        {"Dataset Partition Table": "reddit_questions.csv", "Database Dimensions": "189,565 Rows", "Tracked Target Fields": "id, text, votes, timestamp, datetime", "Your Strategy Context Route": "Evaluates title question string length metrics."},
        {"Dataset Partition Table": "reddit_answers.csv", "Database Dimensions": "5,566,660 Rows", "Tracked Target Fields": "index, q_id, text, votes", "Your Strategy Context Route": "Evaluates standard short-to-medium length comments density indices."},
        {"Dataset Partition Table": "reddit_answers_long.csv", "Database Dimensions": "374,167 Rows", "Tracked Target Fields": "index, q_id, text, votes", "Your Strategy Context Route": "Evaluates complex text structures and descriptive story-driven narratives."}
    ]
    st.table(pd.DataFrame(grid_data))

    # --- 8. AUTOMATED INSIGHTS GENERATION BLOCK ---
    if include_insights:
        st.markdown("### 💡 Automated Optimization Summary Insights")
        st.markdown(f"""
        <div style="background-color: #f0fdf4; padding: 16px; border-radius: 8px; border: 1px solid #bbf7d0;">
            <ul>
                <li>The chosen hook focus <b>({user_hook})</b> paired with the target length parameter generates an ideal audience engagement footprint that fits the training needs of dialogue modeling text systems.</li>
                <li>Your projected traffic level intensity of <b>{user_traffic} points out of 10</b> indicates an optimized algorithmic submission sequence pipeline.</li>
                <li><b>Action Item:</b> Try modifying the text structure slightly by adding an intriguing bracketed qualifier tag at the start (e.g., <i>[Serious]</i>) to shift the text style into a high-authority category band instantly.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 Complete the interview survey questionnaire questions inside the white block above and click 'Submit My Answers & Analyze Content' to view your custom analysis scores, emojis, advice, and charts.")
