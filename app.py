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
    {"id": 13, "type": "picture", "category": "Visual Monuments", "image_url": "
