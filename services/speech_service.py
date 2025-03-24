import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import base64
import os

def text_to_speech(text):
    """Convert text to speech and return the audio file path.
    
    Args:
        text (str): The text to convert to speech
        
    Returns:
        str: Path to the temporary audio file
    """
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        return tmp_file.name

def autoplay_audio(audio_path):
    """Auto-play audio in Streamlit.
    
    Args:
        audio_path (str): Path to the audio file to play
    """
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

def speech_to_text():
    """Convert speech to text using microphone input.
    
    Returns:
        str or None: Transcribed text or None if transcription failed
    """
    r = sr.Recognizer()
    
    # Set the silence threshold to 5 seconds
    r.pause_threshold = 5.0
    
    with sr.Microphone() as source:
        st.write("Listening... Speak now! Recording will automatically stop after 5 seconds of silence.")
        
        # Adjust for ambient noise to improve recognition
        r.adjust_for_ambient_noise(source, duration=1)
        
        # Listen with extended silence threshold
        audio = r.listen(source, timeout=None, phrase_time_limit=None)
        st.write("Processing your speech...")
    
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand your speech.")
        return None
    except sr.RequestError:
        st.error("Could not request results from the speech recognition service.")
        return None

def transcribe_audio_file(file_path):
    """Transcribe an audio file.
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        str or None: Transcribed text or None if transcription failed
    """
    r = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = r.record(source)
            transcription = r.recognize_google(audio_data)
            return transcription
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None