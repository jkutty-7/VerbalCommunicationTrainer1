import os
import json
from datetime import datetime
import uuid
import yaml
import streamlit as st


# Constants
USER_DATA_FILE = 'data/user_data.json'
print(USER_DATA_FILE)
def initialize_user_data():
    """Initialize user data file if it doesn't exist."""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({"users": {}, "sessions": []}, f)

def save_user_data(data):
    """Save user data to file.
    
    Args:
        data (dict): The data to save
    """
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_user_data():
    """Load user data from file.
    
    Returns:
        dict: The loaded user data
    """
    initialize_user_data()
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_session(user_id, activity_type, user_input, ai_feedback):
    """Save session data.
    
    Args:
        user_id (str): The user's ID
        activity_type (str): The type of activity
        user_input (str): The user's input
        ai_feedback (str): The AI's feedback
        
    Returns:
        str: The session ID
    """
    data = load_user_data()
    session_id = str(uuid.uuid4())
    
    session = {
        "id": session_id,
        "user_id": user_id,
        "activity_type": activity_type,
        "user_input": user_input,
        "ai_feedback": ai_feedback,
        "timestamp": datetime.now().isoformat()
    }
    
    data["sessions"].append(session)
    save_user_data(data)
    return session_id

def get_user_sessions(user_id):
    """Get all sessions for a user.
    
    Args:
        user_id (str): The user's ID
        
    Returns:
        list: The user's sessions
    """
    data = load_user_data()
    return [session for session in data["sessions"] if session["user_id"] == user_id]