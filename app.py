import streamlit as st
import os
from dotenv import load_dotenv

# Import modules
from modules.chat_coach import render_chat_coach
from modules.voice_practice import render_voice_practice
from modules.skill_training import render_skill_training
from modules.presentation import render_presentation_assessment
from modules.progress_tracker import render_progress_tracker

# Import services
from services.data_service import initialize_user_data
import uuid

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="Verbal Communication Skills Trainer",
        page_icon="🎤",
        layout="wide"
    )
    
    initialize_user_data()
    
    # Session state variables
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_activity' not in st.session_state:
        st.session_state.current_activity = None
    if 'audio_file' not in st.session_state:
        st.session_state.audio_file = None
    
    # Sidebar for navigation
    st.sidebar.title("Communication Trainer")
    app_mode = st.sidebar.selectbox(
        "Choose a Module",
        ["Home", "Chat Coach", "Voice Practice", "Skill Training", "Presentation Assessment", "Progress Tracker"]
    )
    
    # Home Page
    if app_mode == "Home":
        st.title("Welcome to the Verbal Communication Skills Trainer")
        st.write("""
        This application helps you improve your verbal communication skills through interactive
        exercises, real-time feedback, and structured training modules.
        
        ### Available Modules:
        - **Chat Coach**: Practice conversations with an AI coach that provides feedback
        - **Voice Practice**: Speak directly to the AI and get feedback on your delivery
        - **Skill Training**: Targeted exercises for impromptu speaking, storytelling, and conflict resolution
        - **Presentation Assessment**: Submit a presentation for comprehensive evaluation
        - **Progress Tracker**: View your history and improvement over time
        
        ### Getting Started:
        Select a module from the sidebar to begin your training!
        """)
        
        st.info("This is a prototype application. Your data is stored locally using JSON.")
    
    # Chat Coach
    elif app_mode == "Chat Coach":
        render_chat_coach()
    
    # Voice Practice
    elif app_mode == "Voice Practice":
        render_voice_practice()
    
    # Skill Training
    elif app_mode == "Skill Training":
        render_skill_training()
        
    # Presentation Assessment
    elif app_mode == "Presentation Assessment":
        render_presentation_assessment()
    # Progress Tracker
    elif app_mode == "Progress Tracker":
        render_progress_tracker()

if __name__ == "__main__":
    main()