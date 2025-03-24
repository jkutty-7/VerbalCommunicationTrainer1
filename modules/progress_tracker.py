import streamlit as st

from services.data_service import get_user_sessions

def render_progress_tracker():
    """Render the Progress Tracker module."""
    st.title("Progress Tracker")
    st.write("View your training history and progress over time.")
    
    user_sessions = get_user_sessions(st.session_state.user_id)
    
    if not user_sessions:
        st.info("You haven't completed any training sessions yet. Try out the different modules to see your progress!")
    else:
        # group sessions by activity type
        sessions_by_type = {}
        for session in user_sessions:
            activity_type = session["activity_type"]
            if activity_type not in sessions_by_type:
                sessions_by_type[activity_type] = []
            sessions_by_type[activity_type].append(session)
        
        # display sessions by type
        for activity_type, sessions in sessions_by_type.items():
            st.subheader(f"{activity_type.replace('_', ' ').title()} Sessions ({len(sessions)})")
            
            for i, session in enumerate(sorted(sessions, key=lambda x: x["timestamp"], reverse=True)):
                with st.expander(f"Session {i+1} - {session['timestamp'][:10]}"):
                    st.write("**Your Input:**")
                    st.write(session["user_input"])
                    st.write("**AI Feedback:**")
                    st.write(session["ai_feedback"])