verbal_communication_trainer/
│
├── app.py                      # Main Streamlit application entry point
│
├── config/
│   ├── __init__.py
│   └── config.yaml             # Configuration settings
│
├── data/
│   └── user_data.json          # User data storage
│
├── modules/
│   ├── __init__.py
│   ├── chat_coach.py           # Chat coach module
│   ├── voice_practice.py       # Voice practice module  
│   ├── skill_training.py       # Skill training module
│   ├── presentation.py         # Presentation assessment module
│   └── progress_tracker.py     # Progress tracking module
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py          # LLM API interaction
│   ├── speech_service.py       # Speech-to-text and text-to-speech
│   └── data_service.py         # Data storage and retrieval
│
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Helper functions
│
├── .env                        # Environment variables
│
├── requirements.txt            # Project dependencies
│