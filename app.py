import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# Set page configuration parameters
st.set_page_config(
    page_title="Multi-Round GK Quiz Portal",
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

# Master Question Bank (50 Unique Questions to perfectly support 5 rounds of 10)
MASTER_QUIZ_BANK = [
    {"id": 1, "category": "Astronomy", "question": "Which planet in our solar system is known as the Red Planet?", "accepted_answers": ["mars"], "display_correct": "Mars", "fact": "Mars looks red because of iron oxide (rust) on its surface."},
    {"id": 2, "category": "Geography", "question": "What is the longest river in the world?", "accepted_answers": ["nile", "nile river"], "display_correct": "Nile River", "fact": "The Nile stretches roughly 6,650 kilometers through northeastern Africa."},
    {"id": 3, "category": "Science", "question": "What is the hardest natural substance known on Earth?", "accepted_answers": ["diamond", "diamonds"], "display_correct": "Diamond", "fact": "Diamonds are made of pure carbon atoms tightly packed in a crystal lattice."},
    {"id": 4, "category": "History", "question": "Who was the first President of the United States?", "accepted_answers": ["george washington", "washington"], "display_correct": "George Washington", "fact": "George Washington served from 1789 to 1797."},
    {"id": 5, "category": "Oceanography", "question": "Which ocean is the largest and deepest on Earth?", "accepted_answers": ["pacific", "pacific ocean"], "display_correct": "Pacific Ocean", "fact": "The Pacific Ocean covers over 30% of the Earth's surface."},
    {"id": 6, "category": "Biology", "question": "What is the powerhouse of the cell?", "accepted_answers": ["mitochondria", "mitochondrion"], "display_correct": "Mitochondria", "fact": "Mitochondria generate most of the cell's supply of ATP, used as a source of chemical energy."},
    {"id": 7, "category": "Geography", "question": "What is the capital city of France?", "accepted_answers": ["paris"], "display_correct": "Paris", "fact": "Paris has been a major center of finance, diplomacy, commerce, fashion, and science since the 17th century."},
    {"id": 8, "category": "Chemistry", "question": "What is the chemical symbol for water?", "accepted_answers": ["h2o"], "display_correct": "H2O", "fact": "A molecule of water contains one oxygen and two hydrogen atoms connected by covalent bonds."},
    {"id": 9, "category": "History", "question": "Which empire constructed the Colosseum in Rome?", "accepted_answers": ["roman", "roman empire"], "display_correct": "The Roman Empire", "fact": "The Colosseum could hold an estimated 50,000 to 80,000 spectators during its time."},
    {"id": 10, "category": "Literature", "question": "Who wrote the tragedy play 'Romeo and Juliet'?", "accepted_answers": ["william shakespeare", "shakespeare"], "display_correct": "William Shakespeare", "fact": "Shakespeare wrote Romeo and Juliet early in his career, somewhere between 1591 and 1595."},
    {"id": 11, "category": "Physics", "question": "What force pulls objects toward the center of the Earth?", "accepted_answers": ["gravity", "gravitational force"], "display_correct": "Gravity", "fact": "Gravity is a fundamental interaction that causes mutual attraction between all things with mass or energy."},
    {"id": 12, "category": "Geography", "question": "Which country has the largest population in the world?", "accepted_answers": ["india"], "display_correct": "India", "fact": "India officially surpassed China in population demographics in the mid-2020s."},
    {"id": 13, "category": "Art", "question": "Who painted the famous 'Mona Lisa'?", "accepted_answers": ["leonardo da vinci", "da vinci"], "display_correct": "Leonardo da Vinci", "fact": "The painting is thought to be a portrait of Lisa Gherardini, the wife of Francesco del Giocondo."},
    {"id": 14, "category": "Chemistry", "question": "What is the chemical symbol for Gold?", "accepted_answers": ["au"], "display_correct": "Au", "fact": "Its symbol Au comes from the Latin word 'aurum', meaning shining dawn."},
    {"id": 15, "category": "Astronomy", "question": "What is the name of the closest star to Earth?", "accepted_answers": ["sun", "the sun"], "display_correct": "The Sun", "fact": "The Sun is a nearly perfect ball of hot plasma, heated to incandescence by nuclear fusion reactions in its core."},
    {"id": 16, "category": "History", "question": "In which year did World War II end?", "accepted_answers": ["1945"], "display_correct": "1945", "fact": "World War II officially concluded with the formal signing of surrender documents aboard the USS Missouri on Sept 2, 1945."},
    {"id": 17, "category": "Music", "question": "How many keys are there on a standard classical piano?", "accepted_answers": ["88"], "display_correct": "88", "fact": "A standard piano includes 52 white keys and 36 black keys for a total of 88 keys."},
    {"id": 18, "category": "Zoology", "question": "What is the largest mammal currently alive on Earth?", "accepted_answers": ["blue whale", "whale"], "display_correct": "Blue Whale", "fact": "Blue whales can grow up to 30 meters in length and weigh over 190 short tons."},
    {"id": 19, "category": "Geography", "question": "Which continent is the South Pole located on?", "accepted_answers": ["antarctica"], "display_correct": "Antarctica", "fact": "Antarctica is the coldest, driest, and windiest continent on Earth."},
    {"id": 20, "category": "Science", "question": "What gas do humans need to breathe in to survive?", "accepted_answers": ["oxygen", "o2"], "display_correct": "Oxygen", "fact": "Oxygen is crucial for cellular respiration in most living organisms."},
    {"id": 21, "category": "Technology", "question": "What does 'WWW' stand for in a website URL browser context?", "accepted_answers": ["world wide web"], "display_correct": "World Wide Web", "fact": "The World Wide Web was invented by Sir Tim Berners-Lee in 1989."},
    {"id": 22, "category": "Mathematics", "question": "What is the square root of 144?", "accepted_answers": ["12"], "display_correct": "12", "fact": "$12 \\times 12 = 144$."},
    {"id": 23, "category": "History", "question": "Which country gifted the Statue of Liberty to the United States?", "accepted_answers": ["france"], "display_correct": "France", "fact": "The statue was designed by Frédéric-Auguste Bartholdi and given to commemorate the alliance between the nations."},
    {"id": 24, "category": "Geography", "question": "What is the smallest country in the world by land area?", "accepted_answers": ["vatican city", "vatican"], "display_correct": "Vatican City", "fact": "Vatican City measures just roughly 0.49 square kilometers in total area."},
    {"id": 25, "category": "Botany", "question": "What pigment gives plants their green coloration?", "accepted_answers": ["chlorophyll"], "display_correct": "Chlorophyll", "fact": "Chlorophyll absorbs energy from light, which is fundamental for photosynthesis processes."},
    {"id": 26, "category": "Literature", "question": "Who wrote the fantasy novel series 'Harry Potter'?", "accepted_answers": ["j.k. rowling", "jk rowling", "rowling"], "display_correct": "J.K. Rowling", "fact": "The seven books have sold more than 600 million copies worldwide."},
    {"id": 27, "category": "Anatomy", "question": "What is the largest organ of the human body?", "accepted_answers": ["skin"], "display_correct": "Skin", "fact": "The skin accounts for about 16% of body weight and covers a surface area of close to 2 square meters."},
    {"id": 28, "category": "Sports", "question": "How many players are on the field for one team in a standard soccer match?", "accepted_answers": ["11"], "display_correct": "11", "fact": "A match is played by two teams, each containing a maximum of 11 players, one of whom must be the goalkeeper."},
    {"id": 29, "category": "Meteorology", "question": "What instrument is used by scientists to measure atmospheric air pressure?", "accepted_answers": ["barometer"], "display_correct": "Barometer", "fact": "Evangelista Torricelli is generally credited with inventing the barometer in 1643."},
    {"id": 30, "category": "History", "question": "Who was the ancient queen of Egypt famously associated with Julius Caesar and Mark Antony?", "accepted_answers": ["cleopatra"], "display_correct": "Cleopatra", "fact": "Cleopatra belonged to the Ptolemaic dynasty, a Greek-speaking royal family that ruled Egypt."},
    {"id": 31, "category": "Geography", "question": "What is the highest mountain peak above sea level in the world?", "accepted_answers": ["mount everest", "everest"], "display_correct": "Mount Everest", "fact": "The international border between China and Nepal runs across its summit point."},
    {"id": 32, "category": "Chemistry", "question": "What is the lightest element on the periodic table?", "accepted_answers": ["hydrogen"], "display_correct": "Hydrogen", "fact": "Hydrogen is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass."},
    {"id": 33, "category": "Astronomy", "question": "What galaxy is our solar system located in?", "accepted_answers": ["milky way", "milky way galaxy"], "display_correct": "Milky Way Galaxy", "fact": "The Milky Way is a barred spiral galaxy with an estimated diameter of 100,000–200,000 light-years."},
    {"id": 34, "category": "History", "question": "Who was the primary author of the American Declaration of Independence?", "accepted_answers": ["thomas jefferson", "jefferson"], "display_correct": "Thomas Jefferson", "fact": "Jefferson composed the declaration between June 11 and June 28, 1776."},
    {"id": 35, "category": "Zoology", "question": "What is the only mammal capable of true, sustained flight?", "accepted_answers": ["bat", "bats"], "display_correct": "Bats", "fact": "Bats are more maneuverable fliers than most birds, flying with very long spread-out digits covered with a thin membrane."},
    {"id": 36, "category": "Geography", "question": "Which country is also known as the Land of the Rising Sun?", "accepted_answers": ["japan"], "display_correct": "Japan", "fact": "The kanji characters that make up Japan's name mean 'sun origin', which is why it's often referred to this way."},
    {"id": 37, "category": "Science", "question": "How many bones are there in an average adult human body?", "accepted_answers": ["206"], "display_correct": "206", "fact": "Human infants are born with around 270 bones, which fuse together as the skeleton matures."},
    {"id": 38, "category": "Computer Science", "question": "What does CPU stand for?", "accepted_answers": ["central processing unit"], "display_correct": "Central Processing Unit", "fact": "The CPU performs basic arithmetic, logic, controlling, and input/output operations specified by instructions."},
    {"id": 39, "category": "Mythology", "question": "Who was the supreme king of the gods in ancient Greek mythology?", "accepted_answers": ["zeus"], "display_correct": "Zeus", "fact": "Zeus was revered as a sky and thunder god, ruling from the heights of Mount Olympus."},
    {"id": 40, "category": "Inventions", "question": "Who is universally credited with inventing the telephone?", "accepted_answers": ["alexander graham bell", "alexander bell", "bell"], "display_correct": "Alexander Graham Bell", "fact": "Bell was awarded the first US patent for the telephone in March of 1876."},
    {"id": 41, "category": "Geography", "question": "What is the capital city of Australia?", "accepted_answers": ["canberra"], "display_correct": "Canberra", "fact": "Canberra was selected as a compromise location between rivals Sydney and Melbourne in 1908."},
    {"id": 42, "category": "History", "question": "Which historical figure was famously known as the Maid of Orléans?", "accepted_answers": ["joan of arc", "jeanne d'arc"], "display_correct": "Joan of Arc", "fact": "Joan of Arc was canonized as a saint of the Catholic Church after her role in the Hundred Years' War."},
    {"id": 43, "category": "Art", "question": "Which artist famously cut off part of his own left ear?", "accepted_answers": ["vincent van gogh", "van gogh"], "display_correct": "Vincent van Gogh", "fact": "Van Gogh suffered from severe psychotic episodes and depression throughout his artistic life."},
    {"id": 44, "category": "Oceanography", "question": "What is the name of the deepest known point in the world's oceans?", "accepted_answers": ["mariana trench", "challenger deep"], "display_correct": "Challenger Deep (Mariana Trench)", "fact": "It is located in the Western Pacific Ocean and plunges nearly 11,000 meters down."},
    {"id": 45, "category": "Science", "question": "What temperature is the freezing point of water in degrees Celsius?", "accepted_answers": ["0", "0 degrees celsius", "0 celsius"], "display_correct": "0°C", "fact": "By definition, water freezes at 0 degrees under standard atmospheric pressures."},
    {"id": 46, "category": "Literature", "question": "Who wrote the classic adventure novel 'Moby-Dick'?", "accepted_answers": ["herman melville", "melville"], "display_correct": "Herman Melville", "fact": "The book was initially a commercial failure but is now considered an anchor of American literature."},
    {"id": 47, "category": "Architecture", "question": "In which country can you find the ancient landmark structures of Petra?", "accepted_answers": ["jordan"], "display_correct": "Jordan", "fact": "Petra is famous for its rock-cut architecture and innovative water conduit system."},
    {"id": 48, "category": "Physics", "question": "Which famous scientist formulated the theory of General Relativity?", "accepted_answers": ["albert einstein", "einstein"], "display_correct": "Albert Einstein", "fact": "Einstein revolutionized modern physics with his formulations of relativity and mass-energy equivalence."},
    {"id": 49, "category": "Geography", "question": "Which US state is entirely made up of volcanic islands?", "accepted_answers": ["hawaii"], "display_correct": "Hawaii", "fact": "Hawaii is the only US state located outside North America and the only one that is an island archipelago."},
    {"id": 50, "category": "History", "question": "Who was the leader of the Soviet Union during World War II?", "accepted_answers": ["joseph stalin", "stalin"], "display_correct": "Joseph Stalin", "fact": "Stalin led the Soviet Union through its industrialization and the critical victory over Axis forces."}
]

# --- PERSISTENT SEED & HISTORY STATES LINKED ACROSS ROUNDS ---
if "used_question_ids" not in st.session_state:
    st.session_state.used_question_ids = set()
if "current_round" not in st.session_state:
    st.session_state.current_round = 1
if "round_questions" not in st.session_state:
    st.session_state.round_questions = []

# --- SUB-STEP LEVEL INFRASTRUCTURE TRACKING ---
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
if "round_completed" not in st.session_state:
    st.session_state.round_completed = False

QUESTIONS_PER_ROUND = 10
PASSING_SCORE = 4
MAX_ROUNDS = 5

# --- HELPER FUNCTION: GENERATE 10 UNIQUE QUESTIONS ---
def load_round_questions():
    # Filter out anything that has been globally used in previous rounds
    available_pool = [q for q in MASTER_QUIZ_BANK if q["id"] not in st.session_state.used_question_ids]
    
    # Fallback safety validation layer: if pool runs completely dry, force reset the global exclusion lock tracking array
    if len(available_pool) < QUESTIONS_PER_ROUND:
        st.session_state.used_question_ids = set()
        available_pool = MASTER_QUIZ_BANK
        
    selected = random.sample(available_pool, QUESTIONS_PER_ROUND)
    st.session_state.round_questions = selected
    # Add newly pulled questions straight into global blacklist
    for q in selected:
        st.session_state.used_question_ids.add(q["id"])

# Init active quiz array if empty state registered
if not st.session_state.round_questions:
    load_round_questions()

# --- SIDEBAR PRESENTATION & CONFIGURATION CONTROLS ---
st.sidebar.markdown(f"## 🏅 Stage Level: Round {st.session_state.current_round} / {MAX_ROUNDS}")
st.sidebar.markdown("### 🏆 Round Progress Tracking")
progress_ratio = min(1.0, (st.session_state.current_index) / QUESTIONS_PER_ROUND)
st.sidebar.progress(progress_ratio)

st.sidebar.markdown(f"**Progress Track:** Question {min(QUESTIONS_PER_ROUND, st.session_state.current_index + 1)} of {QUESTIONS_PER_ROUND}")
st.sidebar.markdown(f"**Current Points:** `{st.session_state.score}` / {QUESTIONS_PER_ROUND}")
st.sidebar.markdown(f"**Passing Requirement:** `{PASSING_SCORE}` or more points")

# Reset functions to wipe structural layouts safely
def full_hard_reset():
    st.session_state.used_question_ids = set()
    st.session_state.current_round = 1
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.is_answered = False
    st.session_state.submitted_answer = ""
    st.session_state.round_completed = False
    load_round_questions()

if st.sidebar.button("🔄 Complete System Hard Reset"):
    full_hard_reset()
    trigger_safe_rerun()

# --- MAIN ENGINE HEADER BLOCK ---
st.title("🧠 Open-TextInput GK Quiz & Deep Metrics Portal")
st.write(f"Welcome to **Round {st.session_state.current_round}**. Answer 10 open questions. Score 4 or more points to bypass verification gates!")
st.markdown("---")

# Conditional Logic Routing: Evaluating State Status
if st.session_state.round_completed:
    final_score = st.session_state.score
    passed = final_score >= PASSING_SCORE
    
    if passed:
        if st.session_state.current_round >= MAX_ROUNDS:
            st.balloons()
            st.success("🏆 **GRAND CHAMPION! You completed all 5 rounds successfully and mastered the portal!**")
        else:
            st.success(f"🎉 **Round {st.session_state.current_round} Passed!** Score: `{final_score} / {QUESTIONS_PER_ROUND}`. Ready for the next stage?")
    else:
        st.error(f"❌ **Round Failed.** Score: `{final_score} / {QUESTIONS_PER_ROUND}`. (Needed {PASSING_SCORE}+ points). You must retry this round.")
        st.info("💡 *Don't worry! New questions have been loaded automatically. No repetitions allowed!*")

    # Metrics Display Dashboard Grid
    kpi1, kpi2 = st.columns(2)
    accuracy = (final_score / QUESTIONS_PER_ROUND) * 100
    kpi1.metric("Round Success Scale", f"{final_score} / {QUESTIONS_PER_ROUND}")
    kpi2.metric("Precision Index Value", f"{accuracy:.1f}%")

    # Render Plotly Chart Analysis Tracking Arrays
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        correct_count = len(history_df[history_df["Status Verification"] == "✅ Correct"])
        incorrect_count = len(history_df[history_df["Status Verification"] == "❌ Incorrect"])
    else:
        history_df = pd.DataFrame()
        correct_count, incorrect_count = 0, 0

    st.markdown("### 📈 Verification Audit Performance Metrics")
    fig_summary = go.Figure()
    fig_summary.add_trace(go.Bar(
        x=['Valid Matches', 'Mismatched Inputs'],
        y=[correct_count, incorrect_count],
        marker_color=['#0d9488', '#ef4444'],
        width=0.35
    ))
    fig_summary.update_layout(template="plotly_white", height=300, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_summary, use_container_width=True)

    st.table(history_df)

    # Progression button arrays
    if passed:
        if st.session_state.current_round < MAX_ROUNDS:
            if st.button("Proceed to Next Round ➡️"):
                st.session_state.current_round += 1
                st.session_state.current_index = 0
                st.session_state.score = 0
                st.session_state.history = []
                st.session_state.is_answered = False
                st.session_state.submitted_answer = ""
                st.session_state.round_completed = False
                load_round_questions()  # Pulls fresh non-repeated questions
                trigger_safe_rerun()
        else:
            if st.button("Restart Entire Game Experience 🔄"):
                full_hard_reset()
                trigger_safe_rerun()
    else:
        if st.button("Retry This Round 🔄"):
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.history = []
            st.session_state.is_answered = False
            st.session_state.submitted_answer = ""
            st.session_state.round_completed = False
            load_round_questions()  # Discards failed set, pulls fresh unrepeated ones
            trigger_safe_rerun()

else:
    # Quiz core loop active gameplay evaluation block
    current_question = st.session_state.round_questions[st.session_state.current_index]
    
    st.markdown(f"### 🚀 Evaluating Subject Sector: `{current_question['category']}`")
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown(f"🧬 **Question {st.session_state.current_index + 1} of 10:** {current_question['question']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    user_typed_input = st.text_input(
        "Type your answer text below in the blank field box:",
        value="",
        placeholder="Type response sequence here...",
        disabled=st.session_state.is_answered,
        key=f"q_text_r{st.session_state.current_round}_{st.session_state.current_index}"
    )
    
    st.markdown("---")
    
    if not st.session_state.is_answered:
        if st.button("🎯 Verify & Validate My Typed Answer"):
            if user_typed_input.strip() == "":
                st.warning("⚠️ Text space is currently empty! Please fill in the answer input field first.")
            else:
                st.session_state.submitted_answer = user_typed_input
                st.session_state.is_answered = True
                trigger_safe_rerun()
                
    else:
        final_answer_string = st.session_state.submitted_answer
        user_clean = final_answer_string.strip().lower()
        is_right = user_clean in current_question["accepted_answers"]
        target_display_answer = current_question["display_correct"]
        
        if is_right:
            st.success(f"✨ **Correct! Excellent Precision.** You matched: **{target_display_answer}**.")
        else:
            st.error(f"❌ **Incorrect Match Registered.** You entered: '{final_answer_string}'. Correct answer: **{target_display_answer}**.")
            
        st.markdown(f"""
        <div class="fact-card">
            <div class="fact-title">💡 Did You Know?</div>
            <p style="margin: 0; color: #0f766e; font-size: 15px;">{current_question['fact']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        button_label = "Proceed to Next Question ➡️" if (st.session_state.current_index + 1 < QUESTIONS_PER_ROUND) else "Unlock Performance Summary Board 📊"
        
        if st.button(button_label):
            st.session_state.history.append({
                "Question Index": f"Q-{st.session_state.current_index + 1}",
                "Subject Focus Category": current_question["category"],
                "Your Input Logged": final_answer_string,
                "Expected Core Value": target_display_answer,
                "Status Verification": "✅ Correct" if is_right else "❌ Incorrect"
            })
            
            if is_right:
                st.session_state.score += 1
                
            if st.session_state.current_index + 1 < QUESTIONS_PER_ROUND:
                st.session_state.current_index += 1
                st.session_state.is_answered = False
                st.session_state.submitted_answer = ""
            else:
                st.session_state.round_completed = True
                
            trigger_safe_rerun()
