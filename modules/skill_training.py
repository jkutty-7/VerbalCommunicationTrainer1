import streamlit as st
import yaml
import random

from services.llm_service import get_llm_response
from services.speech_service import speech_to_text
from services.data_service import save_session

# Load config
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

TOPICS_IMPROMPTU = config['content']["topics_impromptu"]
CONFLICT_SCENARIOS = config['content']["conflict_scenarios"]

def render_skill_training():
    """Render the Skill Training module."""
    st.title("Skill Training")
    st.write("Targeted exercises to build specific communication skills.")
    

    skill_type = st.selectbox(
        "Select Skill to Train:",
        ["Impromptu Speaking", "Storytelling", "Conflict Resolution"]
    )
    
    if skill_type == "Impromptu Speaking":
        render_impromptu_speaking()
    elif skill_type == "Storytelling":
        render_storytelling()
    elif skill_type == "Conflict Resolution":
        render_conflict_resolution()

def render_impromptu_speaking():
    """Render the Impromptu Speaking exercise."""
    st.subheader("Impromptu Speaking Exercise")
    st.write("You'll be given a random topic to speak about for 1-2 minutes.")
    
    if st.button("Generate Topic"):
        topic = random.choice(TOPICS_IMPROMPTU)
        st.session_state.current_activity = {"type": "impromptu", "topic": topic}
        st.write(f"**Your Topic:** {topic}")
    
    if st.session_state.current_activity and st.session_state.current_activity["type"] == "impromptu":
        st.write("Enter your response to the topic:")
        

        input_method = st.radio(
            "Choose input method:",
            ["Text", "Voice"],
            key="impromptu_input_method"
        )
        
        
        if "impromptu_response" not in st.session_state:
            st.session_state.impromptu_response = ""
        
        # voice input
        if input_method == "Voice":
            if st.button("Start Recording", key="impromptu_record"):
                user_speech = speech_to_text()
                if user_speech:
                    st.subheader("Your Speech:")
                    st.write(user_speech)
                    st.session_state.impromptu_response = user_speech
        
        # Text area that uses the session state value (works with both text and voice input)
        response = st.text_area(
            "Your response:", 
            value=st.session_state.impromptu_response,
            height=200
        )
        
        if st.button("Submit Response"):
            if response:
                topic = st.session_state.current_activity["topic"]
                system_prompt = config['system_prompt']["impromptu_speaking"].format(topic=topic)
                feedback = get_llm_response(response, system_prompt)
                
                st.subheader("Feedback:")
                st.write(feedback)
                
                save_session(st.session_state.user_id, "impromptu_speaking", 
                            f"Topic: {topic}\nResponse: {response}", feedback)

def render_storytelling():
    """Render the Storytelling exercise."""
    st.subheader("Storytelling Exercise")
    st.write("Narrate a short story (real or fictional) that demonstrates your storytelling ability.")
    
    input_method = st.radio(
        "Choose input method:",
        ["Text", "Voice"],
        key="storytelling_input_method"
    )
    

    if "storytelling_response" not in st.session_state:
        st.session_state.storytelling_response = ""
    
    if input_method == "Voice":
        if st.button("Start Recording", key="storytelling_record"):
            user_speech = speech_to_text()
            if user_speech:
                st.subheader("Your Speech:")
                st.write(user_speech)
                st.session_state.storytelling_response = user_speech
    
    story = st.text_area(
        "Your story:", 
        value=st.session_state.storytelling_response,
        height=250
    )
    
    if st.button("Submit Story"):
        if story:
            system_prompt = config['system_prompt']["storytelling"]
            feedback = get_llm_response(story, system_prompt)
            
            st.subheader("Feedback:")
            st.write(feedback)
            
            save_session(st.session_state.user_id, "storytelling", story, feedback)

def render_conflict_resolution():
    """Render the Conflict Resolution exercise."""
    st.subheader("Conflict Resolution Exercise")
    st.write("Practice responding to a challenging workplace scenario.")
    
    if st.button("Generate Scenario"):
        scenario = random.choice(CONFLICT_SCENARIOS)
        st.session_state.current_activity = {"type": "conflict", "scenario": scenario}
        st.write(f"**Scenario:** {scenario}")
    
    if st.session_state.current_activity and st.session_state.current_activity["type"] == "conflict":
        st.write("Enter your response to the conflict scenario:")
        
        input_method = st.radio(
            "Choose input method:",
            ["Text", "Voice"],
            key="conflict_input_method"
        )
        
        if "conflict_response" not in st.session_state:
            st.session_state.conflict_response = ""
        

        if input_method == "Voice":
            if st.button("Start Recording", key="conflict_record"):
                user_speech = speech_to_text()
                if user_speech:
                    st.subheader("Your Speech:")
                    st.write(user_speech)
                    st.session_state.conflict_response = user_speech
        
    
        response = st.text_area(
            "Your response:", 
            value=st.session_state.conflict_response,
            height=200
        )
        
        if st.button("Submit Response"):
            if response:
                scenario = st.session_state.current_activity["scenario"]
                system_prompt = config['system_prompt']["conflict_resolution"].format(scenario=scenario)
                feedback = get_llm_response(response, system_prompt)
                
                st.subheader("Feedback:")
                st.write(feedback)
                
                # Save session
                save_session(st.session_state.user_id, "conflict_resolution", 
                            f"Scenario: {scenario}\nResponse: {response}", feedback)