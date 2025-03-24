import streamlit as st
import yaml
import tempfile
import os

from services.llm_service import get_llm_response
from services.speech_service import speech_to_text, transcribe_audio_file
from services.data_service import save_session

# Load config
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def render_voice_practice():
    """Render the Voice Practice module."""
    st.title("Voice Practice")
    st.write("Speak directly to the AI and receive feedback on your delivery.")
    
    st.subheader("Choose an option:")
    voice_option = st.radio(
        "How would you like to practice?",
        ["Record Speech", "Upload Audio File"]
    )
    
    if voice_option == "Record Speech":
        if st.button("Start Recording"):
            user_speech = speech_to_text()
            if user_speech:
                st.subheader("Your Speech:")
                st.write(user_speech)
                
                system_prompt = config['system_prompt']["chat_coach"]
                prompt = f"Evaluate this spoken response: {user_speech}"
                feedback = get_llm_response(prompt, system_prompt)
                
                st.subheader("Feedback:")
                st.write(feedback)
                
                save_session(st.session_state.user_id, "voice_practice", user_speech, feedback)
    
    else:
        uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV)", type=["mp3", "wav"])
        if uploaded_file is not None:
            st.audio(uploaded_file)
            
    
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_filename = tmp_file.name
            
            if st.button("Transcribe Audio"):
                st.write("Transcribing audio... Please wait.")
                
                transcription = transcribe_audio_file(temp_filename)
                if transcription:
                    st.session_state.transcription = transcription
                    st.success("Transcription complete!")
            

            if "transcription" not in st.session_state:
                st.session_state.transcription = ""
            
            # display transcription in text area, allowing for edits
            transcription = st.text_area("Audio Transcription (edit if needed):", 
                                        value=st.session_state.transcription,
                                        height=150)
            
            if st.button("Get Feedback") and transcription:

                system_prompt = config['system_prompt']["chat_coach"]
                prompt = f"Evaluate this spoken response (transcribed): {transcription}"
                feedback = get_llm_response(prompt, system_prompt)
                
                st.subheader("Feedback:")
                st.write(feedback)
                

                save_session(st.session_state.user_id, "voice_practice_upload", 
                            transcription, feedback)
            
            if os.path.exists(temp_filename):
                try:
                    os.unlink(temp_filename)
                except:
                    pass