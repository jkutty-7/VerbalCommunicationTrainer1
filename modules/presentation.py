import streamlit as st
import yaml
import tempfile
import os

from services.llm_service import get_llm_response
from services.speech_service import transcribe_audio_file
from services.data_service import save_session

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def render_presentation_assessment():
    """Render the Presentation Assessment module."""
    st.title("Presentation Assessment")
    st.write("Submit a presentation for comprehensive evaluation.")
    
    presentation_type = st.radio(
        "Select Submission Type:",
        ["Text Script", "Audio Recording"]
    )
    
    if presentation_type == "Text Script":
        render_text_presentation()
    else:
        render_audio_presentation()

def render_text_presentation():
    """Render the Text Script submission option."""
    st.subheader("Submit Presentation Script")
    presentation_title = st.text_input("Presentation Title:")
    presentation_script = st.text_area("Paste your presentation script here:", height=300)
    
    if st.button("Submit for Assessment"):
        if presentation_script:
            with st.spinner("Analyzing your presentation..."):
                system_prompt = config['system_prompt']["presentation_assessment"]
                prompt = f"Script:\n{presentation_script}"
                assessment = get_llm_response(prompt, system_prompt)
                
                st.subheader("Assessment Results:")
                st.write(assessment)
                
                save_session(st.session_state.user_id, "presentation_assessment_text", 
                            f"Title: {presentation_title}\nScript: {presentation_script}", assessment)

def render_audio_presentation():
    """Render the Audio Recording submission option."""
    st.subheader("Submit Audio Recording")
    st.write("Upload an audio recording of your presentation.")
    
    uploaded_file = st.file_uploader("Upload presentation (MP3, WAV)", type=["mp3", "wav"])
    
    if uploaded_file is not None:
        st.audio(uploaded_file)
        
        if st.button("Transcribe and Analyze"):
            with st.spinner("Transcribing audio and analyzing presentation..."):
                # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_filename = tmp_file.name
                
                try:
                    # Transcribe the audio file
                    transcription = transcribe_audio_file(temp_filename)
                    
            
                    st.subheader("Transcription:")
                    st.write(transcription)
                    
                    # Get assessment from LLM
                    system_prompt = config['system_prompt']["presentation_assessment"]
                    prompt = f"Transcription:\n{transcription}"
                    assessment = get_llm_response(prompt, system_prompt)
                    
        
                    st.subheader("Assessment Results:")
                    st.write(assessment)
                    
    
                    save_session(st.session_state.user_id, "presentation_assessment_audio", 
                                f"Transcription: {transcription}", assessment)
                
                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")
                
                finally:
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)