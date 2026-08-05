import streamlit as st
from utils.session import init_session_state, require_login, is_generating, set_generating
from utils.styles import apply_custom_styles, show_header, show_model_badge
from utils.api_client import generate_activity

st.set_page_config(page_title="Classroom Activities", page_icon="🎯", layout="wide")
apply_custom_styles()
init_session_state()
require_login()

show_header("Classroom Activities Generator", "Engage your students with fun and interactive activities", "🎯")

with st.form("activity_form"):
    topic = st.text_input("Topic", max_chars=200, placeholder="e.g., The Solar System")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        grade_display = st.selectbox("Grade Level", ["Elementary", "Middle School", "High School"])
        grade_map = {"Elementary": "elementary", "Middle School": "middle", "High School": "high"}
    
    with col2:
        subject_display = st.selectbox("Subject", ["Math", "Science", "English", "History", "Art", "General"])
        subject_map = {"Math": "math", "Science": "science", "English": "english", "History": "history", "Art": "art", "General": "general"}
        
    with col3:
        activity_display = st.selectbox("Activity Type", ["Group Activity", "Discussion", "Role-Play", "Classroom Game", "Assessment", "Exit Ticket"])
        activity_map = {
            "Group Activity": "group_activity", 
            "Discussion": "discussion", 
            "Role-Play": "role_play", 
            "Classroom Game": "classroom_game", 
            "Assessment": "assessment", 
            "Exit Ticket": "exit_ticket"
        }

    submit_button = st.form_submit_button("Generate Activity", disabled=is_generating())

if submit_button:
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        set_generating(True)
        with st.spinner(f"Generating {activity_display.lower()}..."):
            response = generate_activity(
                topic=topic.strip(), 
                grade_level=grade_map[grade_display], 
                subject=subject_map[subject_display],
                activity_type=activity_map[activity_display]
            )
            
        set_generating(False)
        
        if response.get("success"):
            activity_content = response["data"]["activity"]
            st.session_state["last_activity"] = activity_content
            st.success(f"{activity_display} generated successfully!")
            show_model_badge(response.get("model_used", ""))
            
            st.markdown(f"### Generated {activity_display}")
            st.markdown(activity_content)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download as Markdown", activity_content, "activity.md", "text/markdown")
            with col2:
                st.download_button("Download as Text", activity_content, "activity.txt", "text/plain")
        else:
            st.error(response.get("message", "Failed to generate activity."))

elif st.session_state.get("last_activity"):
    st.markdown("### Previous Activity")
    st.markdown(st.session_state["last_activity"])
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download as Markdown", st.session_state["last_activity"], "activity.md", "text/markdown")
    with col2:
        st.download_button("Download as Text", st.session_state["last_activity"], "activity.txt", "text/plain")
