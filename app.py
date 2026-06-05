import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# Set page configuration parameters
st.set_page_config(
    page_title="Advanced Multi-Type GK Quiz Portal",
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
    .group-box {
        background-color: #f8fafc;
        padding: 12px;
        border-radius: 8px;
        border: 1px dashed #cbd5e1;
        margin-bottom: 15px;
        font-weight: 500;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# --- MASTER QUIZ BANK WITH 50 FULLY VALIDATED UNIQUE ITEMS ---
MASTER_QUIZ_BANK = [
    # TYPE 1: TEXT QUESTIONS
    {"id": 1, "type": "text", "category": "Astronomy", "question": "Which planet in our solar system is known as the Red Planet?", "accepted_answers": ["mars"], "display_correct": "Mars", "fact": "Mars looks red because of iron oxide (rust) on its surface."},
    {"id": 2, "type": "text", "category": "Geography", "question": "What is the longest river in the world?", "accepted_answers": ["nile", "nile river"], "display_correct": "Nile River", "fact": "The Nile stretches roughly 6,650 kilometers through northeastern Africa."},
    {"id": 3, "type": "text", "category": "Science", "question": "What is the hardest natural substance known on Earth?", "accepted_answers": ["diamond", "diamonds"], "display_correct": "Diamond", "fact": "Diamonds are made of pure carbon atoms tightly packed in a crystal lattice."},
    {"id": 4, "type": "text", "category": "History", "question": "Who was the first President of the United States?", "accepted_answers": ["george washington", "washington"], "display_correct": "George Washington", "fact": "George Washington served from 1789 to 1797."},
    {"id": 5, "type": "text", "category": "Oceanography", "question": "Which ocean is the largest and deepest on Earth?", "accepted_answers": ["pacific", "pacific ocean"], "display_correct": "Pacific Ocean", "fact": "The Pacific Ocean covers over 30% of the Earth's surface."},
    {"id": 6, "type": "text", "category": "Biology", "question": "What is considered the master powerhouse component of the living cell?", "accepted_answers": ["mitochondria", "mitochondrion"], "display_correct": "Mitochondria", "fact": "Mitochondria generate most of the cell's structural chemical energy reserves."},
    {"id": 7, "type": "text", "category": "Chemistry", "question": "What is the base molecular chemical symbol for pure water?", "accepted_answers": ["h2o"], "display_correct": "H2O", "fact": "A molecule of water contains one oxygen and two hydrogen atoms connected by covalent bonds."},
    {"id": 8, "type": "text", "category": "Art", "question": "Which legendary Renaissance artist painted the famous 'Mona Lisa' portrait?", "accepted_answers": ["leonardo da vinci", "da vinci"], "display_correct": "Leonardo da Vinci", "fact": "The painting is thought to be a portrait of Lisa Gherardini."},
    {"id": 9, "type": "text", "category": "Anatomy", "question": "What is the single largest organ of the human body?", "accepted_answers": ["skin"], "display_correct": "Skin", "fact": "The skin accounts for about 16% of entire human adult body weight structural volume."},
    {"id": 10, "type": "text", "category": "Physics", "question": "Which famous scientist formulated the structural theory of General Relativity?", "accepted_answers": ["albert einstein", "einstein"], "display_correct": "Albert Einstein", "fact": "Einstein revolutionized modern physics with his formulations of relativity."},

    # TYPE 2: PICTURE / VISUAL PUZZLES
    {"id": 11, "type": "picture", "category": "Visual Landmarks", "image_url": "https://images.unsplash.com/photo-1543349689-9a4d426bee8e?w=500", "question": "Identify this historic European iron tower structure located in Paris:", "accepted_answers": ["eiffel tower", "eiffel"], "display_correct": "Eiffel Tower", "fact": "Completed in 1889, it was built as the entrance arch for the World's Fair."},
    {"id": 12, "type": "picture", "category": "Visual Landmarks", "image_url": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=500", "question": "Identify this white marble monument built by Shah Jahan in Agra, India:", "accepted_answers": ["taj mahal", "tajmahal"], "display_correct": "Taj Mahal", "fact": "It was commissioned in 1531 to house the tomb of his favorite wife, Mumtaz Mahal."},
    {"id": 13, "type": "picture", "category": "Visual Monuments", "image_url": "https://images.unsplash.com/photo-1605538032432-a9f0c8d9baac?w=500", "question": "Identify this historic colossal neoclassical sculpture situated on Liberty Island in New York Harbor:", "accepted_answers": ["statue of liberty", "liberty"], "display_correct": "Statue of Liberty", "fact": "A gift from the people of France to the United States, designed by Frédéric-Auguste Bartholdi."},
    {"id": 14, "type": "picture", "category": "Visual Wonders", "image_url": "https://images.unsplash.com/photo-1608958416715-bc4404fa77df?w=500", "question": "Identify this ancient amphitheatre located in the center of Rome, Italy:", "accepted_answers": ["colosseum", "coliseum"], "display_correct": "The Colosseum", "fact": "It is the largest ancient amphitheatre ever built, and is still the largest standing amphitheatre in the world today."},
    {"id": 15, "type": "picture", "category": "Visual Nature Puzzles", "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500", "question": "Look at this runner. What primary human structural protein component makes up human hair, nails, and outer claws?", "accepted_answers": ["keratin"], "display_correct": "Keratin", "fact": "Keratin protects epithelial cells from damage or stress structural anomalies."},
    {"id": 16, "type": "picture", "category": "Visual Icons", "image_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=500", "question": "This abstract fluid structure mimics code patterns. What computing term describes a self-replicating malicious code segment?", "accepted_answers": ["virus", "computer virus"], "display_correct": "Virus", "fact": "The first computer virus was created in 1971 and was named the Creeper program."},
    {"id": 17, "type": "picture", "category": "Visual Astronomy", "image_url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=500", "question": "Look at this image of our home planet. What percentage of Earth's surface is covered by liquid water? (Answer with the whole number percentage, e.g., 71)", "accepted_answers": ["71", "71%"], "display_correct": "71%", "fact": "About 71 percent of the Earth's surface is water-covered, and the oceans hold about 96.5 percent of all Earth's water."},
    {"id": 18, "type": "picture", "category": "Visual Archeology", "image_url": "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=500", "question": "Identify the ancient structural wonders shown in this desert setting:", "accepted_answers": ["pyramids", "egyptian pyramids", "pyramids of giza"], "display_correct": "The Pyramids of Giza", "fact": "The Great Pyramid was built for the Fourth Dynasty Pharaoh Khufu and is the oldest of the Seven Wonders of the Ancient World."},
    {"id": 19, "type": "picture", "category": "Visual Engineering", "image_url": "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=500", "question": "Look at these music headphones. What wireless standard named after a 10th-century Scandinavian king allows short-range digital audio transmission?", "accepted_answers": ["bluetooth"], "display_correct": "Bluetooth", "fact": "Bluetooth was named after King Harald Bluetooth, who united Scandinavian tribes just as the technology unites communication protocols."},
    {"id": 20, "type": "picture", "category": "Visual Architecture", "image_url": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=500", "question": "This motorcycle represents custom vehicle mechanics. What internal component converts chemical engine explosions into wheels spinning?", "accepted_answers": ["piston", "pistons"], "display_correct": "Piston", "fact": "Pistons transmit force from expanding gas in the cylinder to the crankshaft via a connecting rod."},

    # TYPE 3: GROUP CLASSIFICATION / SEGMENTATION CATEGORY MAPPING PUZZLES
    {"id": 21, "type": "group", "category": "Platform Mapping", "items": ["WhatsApp", "Email", "Slack"], "question": "What functional industry segment classification category do WhatsApp, Email, and Slack belong to?", "accepted_answers": ["messaging", "communication", "chat"], "display_correct": "Messaging / Communication", "fact": "These applications utilize synchronized protocol gateways to distribute written messaging assets."},
    {"id": 22, "type": "group", "category": "Platform Mapping", "items": ["YouTube", "Instagram", "TikTok"], "question": "What functional category domain do YouTube, Instagram, and TikTok belong to?", "accepted_answers": ["entertainment", "entertaining", "social media"], "display_correct": "Entertainment / Social Media", "fact": "These platforms optimize algorithmic video matrices to engage consumers looking for dynamic content feeds."},
    {"id": 23, "type": "group", "category": "Platform Mapping", "items": ["Spotify", "Apple Music", "SoundCloud"], "question": "What operational digital stream classification do Spotify, Apple Music, and SoundCloud belong to?", "accepted_answers": ["audio streaming", "music", "audio", "music streaming"], "display_correct": "Audio / Music Streaming", "fact": "They serve cloud-hosted catalog assets securely using compressed audio codecs over distributed server hubs."},
    {"id": 24, "type": "group", "category": "Science Mapping", "items": ["Oxygen", "Hydrogen", "Nitrogen"], "question": "What structural phase group state do Oxygen, Hydrogen, and Nitrogen classify as under standard room conditions?", "accepted_answers": ["gas", "gases", "gas state"], "display_correct": "Gases", "fact": "These elements exhibit highly dispersed molecular spacing with negligible intermolecular bounds at room temperature."},
    {"id": 25, "type": "group", "category": "Financial Mapping", "items": ["Bitcoin", "Ethereum", "Solana"], "question": "What modern asset classification category do Bitcoin, Ethereum, and Solana belong to?", "accepted_answers": ["cryptocurrency", "crypto", "cryptocurrencies"], "display_correct": "Cryptocurrency", "fact": "These digital assets rely on cryptography and decentralized consensus mechanics to secure transactions on a blockchain."},
    {"id": 26, "type": "group", "category": "Hardware Mapping", "items": ["Keyboard", "Mouse", "Microphone"], "question": "In hardware terms, what structural operational component category group do Keyboards, Mice, and Microphones belong to?", "accepted_answers": ["input devices", "input", "input device"], "display_correct": "Input Devices", "fact": "Input devices convert user-generated interactions into binary signals parsed by the CPU processing engine."},
    {"id": 27, "type": "group", "category": "Hardware Mapping", "items": ["Monitor", "Printer", "Speakers"], "question": "In hardware terms, what functional classification group do Monitors, Printers, and Speakers belong to?", "accepted_answers": ["output devices", "output", "output device"], "display_correct": "Output Devices", "fact": "Output devices translate computed data blocks into human-readable physical form factors like pixels, ink, or acoustic sound waves."},
    {"id": 28, "type": "group", "category": "E-Commerce Mapping", "items": ["Amazon", "eBay", "Shopify"], "question": "What macro business industry cluster segment do Amazon, eBay, and Shopify belong to?", "accepted_answers": ["e-commerce", "ecommerce", "online retail", "retail"], "display_correct": "E-Commerce", "fact": "These organizations facilitate the exchange of goods and services globally using digital transaction ledgers and storefront designs."},
    {"id": 29, "type": "group", "category": "Biology Mapping", "items": ["Lion", "Tiger", "Wolf"], "question": "Based on nutritional dietary classification, what group cluster do Lions, Tigers, and Wolves belong to?", "accepted_answers": ["carnivore", "carnivores", "meat eaters"], "display_correct": "Carnivores", "fact": "Carnivores are organisms that derive their energy and nutrient requirements from a diet consisting exclusively or mainly of animal tissue."},
    {"id": 30, "type": "group", "category": "Software Mapping", "items": ["Linux", "Windows", "macOS"], "question": "What system software group architecture classification layer do Linux, Windows, and macOS belong to?", "accepted_answers": ["operating system", "operating systems", "os"], "display_correct": "Operating Systems", "fact": "Operating systems manage machine hardware resources directly and abstract system pathways for application software execution layers."},
    
    # TYPE 1 CONTINUED (Fixed with explicit "type": "text")
    {"id": 31, "type": "text", "category": "Geography", "question": "What is the capital city of France?", "accepted_answers": ["paris"], "display_correct": "Paris", "fact": "Paris is a global hub for art, fashion, gastronomy, and culture."},
    {"id": 32, "type": "text", "category": "History", "question": "In which calendar year did World War II officially conclude?", "accepted_answers": ["1945"], "display_correct": "1945", "fact": "The war ended with the formal signing of surrender documents in September 1945."},
    {"id": 33, "type": "text", "category": "Geography", "question": "Which specific country has the largest population metrics in the world?", "accepted_answers": ["india"], "display_correct": "India", "fact": "India officially surpassed other demographics to take the top population position in the mid-2020s."},
    {"id": 34, "type": "text", "category": "Mathematics", "question": "What is the square root valuation of the integer 144?", "accepted_answers": ["12"], "display_correct": "12", "fact": "Twelve multiplied by itself yields exactly 144."},
    {"id": 35, "type": "text", "category": "Geography", "question": "What is the smallest sovereign country in the world by total land area maps?", "accepted_answers": ["vatican city", "vatican"], "display_correct": "Vatican City", "fact": "Vatican City measures just roughly 0.49 square kilometers in total area footprint."},
    {"id": 36, "type": "text", "category": "Botany", "question": "What biological pigment gives plants their characteristic green coloration?", "accepted_answers": ["chlorophyll"], "display_correct": "Chlorophyll", "fact": "Chlorophyll permits plants to absorb energy efficiently from light during photosynthesis cycles."},
    {"id": 37, "type": "text", "category": "Sports", "question": "How many active players are fielded for one team simultaneously during a standard soccer match?", "accepted_answers": ["11"], "display_correct": "11", "fact": "A match is maintained by two competing blocks containing a maximum of 11 players each."},
    {"id": 38, "type": "text", "category": "Meteorology", "question": "What scientific instrument measures atmospheric air pressure shifts?", "accepted_answers": ["barometer"], "display_correct": "Barometer", "fact": "Evangelista Torricelli is credited with engineering the initial operational barometer format in 1643."},
    {"id": 39, "type": "text", "category": "Chemistry", "question": "What is the lightest elemental atomic structure listed on the Periodic Table?", "accepted_answers": ["hydrogen"], "display_correct": "Hydrogen", "fact": "Hydrogen makes up roughly 75% of all standard scenic cosmic mass structures."},
    {"id": 40, "type": "text", "category": "Astronomy", "question": "What named spiral galaxy contains our specific solar system profile?", "accepted_answers": ["milky way", "milky way galaxy"], "display_correct": "Milky Way Galaxy", "fact": "The Milky Way is a barred spiral system estimated to contain hundreds of billions of stars."},
    
    # TYPE 3 CONTINUED: MORE GROUPS
    {"id": 41, "type": "group", "category": "Automotive Mapping", "items": ["Tesla", "Ford", "Toyota"], "question": "What manufacturing industry grouping classification do Tesla, Ford, and Toyota belong to?", "accepted_answers": ["automotive", "car manufacturers", "automakers", "cars"], "display_correct": "Automotive / Car Manufacturers", "fact": "These entities specialize in mass engineering, assembly, and sales of motor vehicles globally."},
    {"id": 42, "type": "group", "category": "Food Mapping", "items": ["Cheddar", "Gouda", "Mozzarella"], "question": "What dairy product culinary class group do Cheddar, Gouda, and Mozzarella belong to?", "accepted_answers": ["cheese", "cheeses"], "display_correct": "Cheese", "fact": "These products are made from cookies or milk proteins separated from liquid whey elements."},
    {"id": 43, "type": "group", "category": "Currency Mapping", "items": ["Dollar", "Euro", "Yen"], "question": "What legal fiscal tender categorization classification group do the Dollar, Euro, and Yen belong to?", "accepted_answers": ["currency", "currencies", "money", "fiat"], "display_correct": "Currencies / Fiat Money", "fact": "Currencies represent centralized economic units of account recognized as legal tender values by state systems."},
    {"id": 44, "type": "group", "category": "Language Mapping", "items": ["Python", "Java", "C++"], "question": "What technical engineering software group taxonomy do Python, Java, and C++ belong to?", "accepted_answers": ["programming languages", "programming language", "code", "coding languages"], "display_correct": "Programming Languages", "fact": "These semantic syntax standards translate instructions into logical instructions machine hardware execution stacks process."},
    {"id": 45, "type": "group", "category": "Season Mapping", "items": ["Summer", "Autumn", "Winter"], "question": "What recurring annual climate division category cycle do Summer, Autumn, and Winter belong to?", "accepted_answers": ["seasons", "season"], "display_correct": "Seasons", "fact": "Seasons result from the Earth's axial tilt relative to its orbital plain trajectory around the Sun."},
    
    # TYPE 2 CONTINUED: MORE PICTURES
    {"id": 46, "type": "picture", "category": "Visual Aviation", "image_url": "https://images.unsplash.com/photo-1540962351504-03099e0a754b?w=500", "question": "Identify what mode of modern commercial long-distance aerodynamic sky transport is pictured here:", "accepted_answers": ["airplane", "aeroplane", "plane", "aircraft"], "display_correct": "Airplane", "fact": "The Wright brothers achieved the first sustained, controlled, powered heavier-than-air manned flight in 1903."},
    {"id": 47, "type": "picture", "category": "Visual Art", "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=500", "question": "This abstract design utilizes colored materials. What physical painting fluid mixture consists of pigments suspended in drying oils?", "accepted_answers": ["oil paint", "oil paints", "oil painting"], "display_correct": "Oil Paint", "fact": "Oil paints became the principal medium used for creating artworks in Europe during the 15th century."},
    {"id": 48, "type": "picture", "category": "Visual Instruments", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500", "question": "Look at this vocal studio tool. What device is used to transform sonic acoustic wave vibrations into electrical signals?", "accepted_answers": ["microphone", "mic"], "display_correct": "Microphone", "fact": "The carbon microphone was independently developed by David Edward Hughes and Thomas Edison in the late 1870s."},
    {"id": 49, "type": "picture", "category": "Visual Nature", "image_url": "https://images.unsplash.com/photo-1528183429752-a97d0bf99b5a?w=500", "question": "Identify this organic plant organism form factor that produces oxygen via light absorption:", "accepted_answers": ["tree", "trees", "plant"], "display_correct": "Tree", "fact": "Trees act as significant carbon sinks, locking up atmospheric carbon dioxide in wood tissue matrices."},
    {"id": 50, "type": "picture", "category": "Visual Chronology", "image_url": "https://images.unsplash.com/photo-1508962914676-134849a727f0?w=500", "question": "Identify what mechanical measurement tracker device is shown monitoring temporal units here:", "accepted_answers": ["watch", "pocket watch", "clock", "timepiece"], "display_correct": "Watch / Pocket Watch", "fact": "Mechanical portable timepieces developed in Europe during the 15th-century evolved into wearable wrist-mounted accessories."}
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

# --- HELPER FUNCTION: GENERATE 10 BALANCED UNIQUE QUESTIONS ---
def load_round_questions():
    available_pool = [q for q in MASTER_QUIZ_BANK if q["id"] not in st.session_state.used_question_ids]
    
    if len(available_pool) < QUESTIONS_PER_ROUND:
        st.session_state.used_question_ids = set()
        available_pool = MASTER_QUIZ_BANK
        
    selected = random.sample(available_pool, QUESTIONS_PER_ROUND)
    st.session_state.round_questions = selected
    
    for q in selected:
        st.session_state.used_question_ids.add(q["id"])

if not st.session_state.round_questions:
    load_round_questions()

# --- SIDEBAR PRESENTATION & CONFIGURATION CONTROLS ---
st.sidebar.markdown(f"## 🏅 Game State: Round {st.session_state.current_round} / {MAX_ROUNDS}")
st.sidebar.markdown("### 🏆 Round Progress Tracking")
progress_ratio = min(1.0, (st.session_state.current_index) / QUESTIONS_PER_ROUND)
st.sidebar.progress(progress_ratio)

st.sidebar.markdown(f"**Progress Track:** Question {min(QUESTIONS_PER_ROUND, st.session_state.current_index + 1)} of {QUESTIONS_PER_ROUND}")
st.sidebar.markdown(f"**Current Points:** `{st.session_state.score}` / {QUESTIONS_PER_ROUND}")
st.sidebar.markdown(f"**Passing Requirement:** `{PASSING_SCORE}` or more points")

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
st.title("🧠 Advanced Multi-Type GK Quiz & Puzzle Portal")
st.write(f"Evaluating **Round {st.session_state.current_round}**. Answer the mixed text, image puzzles, and group classification prompts correctly!")
st.markdown("---")

if st.session_state.round_completed:
    final_score = st.session_state.score
    passed = final_score >= PASSING_SCORE
    
    if passed:
        if st.session_state.current_round >= MAX_ROUNDS:
            st.balloons()
            st.success("🏆 **GRAND MASTER CHAMPION! You completed all 5 rounds across text, visual, and sorting modules successfully!**")
        else:
            st.success(f"🎉 **Round {st.session_state.current_round} Successfully Cleared!** Score: `{final_score} / {QUESTIONS_PER_ROUND}`.")
    else:
        st.error(f"❌ **Round Failed.** Your Score: `{final_score} / {QUESTIONS_PER_ROUND}`. (Target requirement: {PASSING_SCORE}+ points).")
        st.info("💡 *Non-repetition clause active: New alternate questions have been drawn for your retry attempt.*")

    kpi1, kpi2 = st.columns(2)
    accuracy = (final_score / QUESTIONS_PER_ROUND) * 100
    kpi1.metric("Validation Accuracy", f"{accuracy:.1f}%")
    kpi2.metric("Round Result Flag", "PASSED 👍" if passed else "FAILED 👎")

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
    fig_summary.update_layout(template="plotly_white", height=280, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_summary, use_container_width=True)

    st.table(history_df)

    if passed:
        if st.session_state.current_round < MAX_ROUNDS:
            if st.button("Unlock and Move to Next Round ➡️"):
                st.session_state.current_round += 1
                st.session_state.current_index = 0
                st.session_state.score = 0
                st.session_state.history = []
                st.session_state.is_answered = False
                st.session_state.submitted_answer = ""
                st.session_state.round_completed = False
                load_round_questions()
                trigger_safe_rerun()
        else:
            if st.button("Reset Entire Application 🔄"):
                full_hard_reset()
                trigger_safe_rerun()
    else:
        if st.button("Retry This Specific Round 🔄"):
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.history = []
            st.session_state.is_answered = False
            st.session_state.submitted_answer = ""
            st.session_state.round_completed = False
            load_round_questions()
            trigger_safe_rerun()

else:
    current_question = st.session_state.round_questions[st.session_state.current_index]
    
    # SAFE FIX: Using .get() fallback parameter to stop KeyError crashes completely
    q_type = current_question.get("type", "text").upper()
    q_category = current_question.get("category", "General Knowledge")
    
    st.markdown(f"### 🚀 Sector focus: `{q_category}` | Type: `{q_type} PUZZLE`")
    
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown(f"🧬 **Question {st.session_state.current_index + 1} of 10:** {current_question.get('question', '')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if current_question.get("type") == "picture":
        st.image(current_question.get("image_url", ""), width=450, caption="Visual Reference Asset Puzzle Hint")
        
    elif current_question.get("type") == "group":
        st.write("🧩 **Group Items To Classify:**")
        group_items = current_question.get("items", [])
        cols = st.columns(max(1, len(group_items)))
        for idx, item in enumerate(group_items):
            with cols[idx]:
                st.markdown(f'<div class="group-box">📦 {item}</div>', unsafe_allow_html=True)

    user_typed_input = st.text_input(
        "Type your validation answer string key below:",
        value="",
        placeholder="Type response sequence here...",
        disabled=st.session_state.is_answered,
        key=f"q_field_r{st.session_state.current_round}_{st.session_state.current_index}"
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
        accepted = current_question.get("accepted_answers", [])
        is_right = user_clean in accepted
        target_display_answer = current_question.get("display_correct", "")
        
        if is_right:
            st.success(f"✨ **Correct! Excellent Analytical Precision.** You correctly targeted: **{target_display_answer}**.")
        else:
            st.error(f"❌ **Incorrect Registration.** You entered: '{final_answer_string}'. Target category mapping: **{target_display_answer}**.")
            
        st.markdown(f"""
        <div class="fact-card">
            <div class="fact-title">💡 Contextual Insight Core Info:</div>
            <p style="margin: 0; color: #0f766e; font-size: 15px;">{current_question.get('fact', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        button_label = "Proceed to Next Question ➡️" if (st.session_state.current_index + 1 < QUESTIONS_PER_ROUND) else "Unlock Performance Summary Board 📊"
        
        if st.button(button_label):
            st.session_state.history.append({
                "Question Index": f"Q-{st.session_state.current_index + 1}",
                "Type Pattern": q_type,
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
