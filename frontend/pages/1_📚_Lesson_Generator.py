import streamlit as st
from utils.session import init_session_state, require_login, is_generating, set_generating
from utils.styles import apply_custom_styles, show_header, show_model_badge
from utils.api_client import generate_lesson

st.set_page_config(page_title="Lesson Generator", page_icon="📚", layout="wide")
apply_custom_styles()
init_session_state()
require_login()

show_header("Lesson Plan Generator", "Create comprehensive lesson plans in seconds", "📚")

with st.form("lesson_form"):
    topic = st.text_input("Topic", max_chars=200, placeholder="e.g., The Water Cycle, Fractions, Causes of WW2")
    
    col1, col2 = st.columns(2)
    with col1:
        grade_display = st.selectbox("Grade Level", ["Elementary", "Middle School", "High School"])
        grade_map = {"Elementary": "elementary", "Middle School": "middle", "High School": "high"}
    
    with col2:
        subject_display = st.selectbox("Subject", ["Math", "Science", "English", "History", "Art", "General"])
        subject_map = {"Math": "math", "Science": "science", "English": "english", "History": "history", "Art": "art", "General": "general"}
        
    submit_button = st.form_submit_button("Generate Lesson Plan", disabled=is_generating())

if submit_button:
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        set_generating(True)
        with st.spinner("Generating lesson plan..."):
            response = generate_lesson(
                topic=topic.strip(), 
                grade_level=grade_map[grade_display], 
                subject=subject_map[subject_display]
            )
            
        set_generating(False)
        
        if response.get("success"):
            lesson_plan = response["data"]["lesson_plan"]
            st.session_state["last_lesson_plan"] = lesson_plan
            st.success("Lesson plan generated successfully!")
            show_model_badge(response.get("model_used", ""))
            
            st.markdown("### Generated Lesson Plan")
            st.markdown(lesson_plan)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download as Markdown",
                    data=lesson_plan,
                    file_name="lesson_plan.md",
                    mime="text/markdown"
                )
            with col2:
                st.download_button(
                    label="Download as Text",
                    data=lesson_plan,
                    file_name="lesson_plan.txt",
                    mime="text/plain"
                )
                
            st.info("💡 You can now generate a quiz from this lesson plan on the Quiz Generator page.")
        else:
            st.error(response.get("message", "Failed to generate lesson plan."))

elif st.session_state.get("last_lesson_plan"):
    st.markdown("### Previous Lesson Plan")
    st.markdown(st.session_state["last_lesson_plan"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download as Markdown",
            data=st.session_state["last_lesson_plan"],
            file_name="lesson_plan.md",
            mime="text/markdown"
        )
    with col2:
        st.download_button(
            label="Download as Text",
            data=st.session_state["last_lesson_plan"],
            file_name="lesson_plan.txt",
            mime="text/plain"
        )
