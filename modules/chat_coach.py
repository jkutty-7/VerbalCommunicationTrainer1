import streamlit as st
import yaml

from services.llm_service import get_llm_response
from services.data_service import save_session


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def render_chat_coach():
    """Render the Chat Coach module."""
    st.title("Chat Coach")
    st.write("Practice your written communication skills with feedback on tone, clarity, and effectiveness.")
    
    coach_type = st.radio(
        "Select Coach Type:",
        ["Communication Coach", "Job Interviewer"]
    )
    
    if "communication_coach_history" not in st.session_state:
        st.session_state.communication_coach_history = []
    
    if "job_interviewer_history" not in st.session_state:
        st.session_state.job_interviewer_history = []
    
    if coach_type == "Communication Coach":
        current_chat_history = st.session_state.communication_coach_history
        system_prompt = config['system_prompt']['chat_coach']
    else: 
        current_chat_history = st.session_state.job_interviewer_history
        system_prompt = config['system_prompt']['interviewer']
    
    if st.button("Clear Chat"):
        if coach_type == "Communication Coach":
            st.session_state.communication_coach_history = []
        else:
            st.session_state.job_interviewer_history = []
        st.rerun()
    
    # Display current chat history
    for message in current_chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**Coach:** {message['content']}")
    

    user_input = st.text_input("Your message:")
    
 
    if st.button("Send"):
        if user_input:
            # Add user message to chat history
            current_chat_history.append({"role": "user", "content": user_input})
            
            full_prompt = user_input
            if len(current_chat_history) > 2:
                context = "\n\n".join([f"{'User' if msg['role'] == 'user' else 'Coach'}: {msg['content']}" 
                                      for msg in current_chat_history[-4:]])
                full_prompt = f"Previous context:\n{context}\n\nCurrent message:\n{user_input}"
            
            coach_response = get_llm_response(full_prompt, system_prompt)
            
            # Add coach response to chat history
            current_chat_history.append({"role": "assistant", "content": coach_response})
            
            save_session(st.session_state.user_id, f"chat_{coach_type.lower().replace(' ', '_')}", 
                         user_input, coach_response)
            
            # Update the specific chat history in session state
            if coach_type == "Communication Coach":
                st.session_state.communication_coach_history = current_chat_history
            else:
                st.session_state.job_interviewer_history = current_chat_history
            
            # Refresh the page to show the updated chat
            st.rerun()