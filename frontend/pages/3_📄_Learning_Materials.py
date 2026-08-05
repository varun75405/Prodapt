import streamlit as st
from utils.session import init_session_state, require_login, is_generating, set_generating
from utils.styles import apply_custom_styles, show_header, show_model_badge
from utils.api_client import generate_material

st.set_page_config(page_title="Learning Materials", page_icon="📄", layout="wide")
apply_custom_styles()
init_session_state()
require_login()

show_header("Learning Materials Generator", "Create worksheets, notes, and handouts", "📄")

with st.form("material_form"):
    topic = st.text_input("Topic", max_chars=200, placeholder="e.g., Photosynthesis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        grade_display = st.selectbox("Grade Level", ["Elementary", "Middle School", "High School"])
        grade_map = {"Elementary": "elementary", "Middle School": "middle", "High School": "high"}
    
    with col2:
        subject_display = st.selectbox("Subject", ["Math", "Science", "English", "History", "Art", "General"])
        subject_map = {"Math": "math", "Science": "science", "English": "english", "History": "history", "Art": "art", "General": "general"}
        
    with col3:
        material_display = st.selectbox("Material Type", ["Worksheet", "Study Notes", "Flashcards", "Practice Exercises", "Homework Assignment", "Classroom Handout"])
        material_map = {
            "Worksheet": "worksheet", 
            "Study Notes": "notes", 
            "Flashcards": "flashcards", 
            "Practice Exercises": "practice_exercises", 
            "Homework Assignment": "homework", 
            "Classroom Handout": "handouts"
        }

    submit_button = st.form_submit_button("Generate Material", disabled=is_generating())

if submit_button:
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        set_generating(True)
        with st.spinner(f"Generating {material_display.lower()}..."):
            response = generate_material(
                topic=topic.strip(), 
                grade_level=grade_map[grade_display], 
                subject=subject_map[subject_display],
                material_type=material_map[material_display]
            )
            
        set_generating(False)
        
        if response.get("success"):
            material_content = response["data"]["content"]
            st.session_state["last_material"] = material_content
            st.success(f"{material_display} generated successfully!")
            show_model_badge(response.get("model_used", ""))
            
            st.markdown(f"### Generated {material_display}")
            st.markdown(material_content)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download as Markdown", material_content, "material.md", "text/markdown")
            with col2:
                st.download_button("Download as Text", material_content, "material.txt", "text/plain")
        else:
            st.error(response.get("message", "Failed to generate material."))

elif st.session_state.get("last_material"):
    st.markdown("### Previous Material")
    st.markdown(st.session_state["last_material"])
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download as Markdown", st.session_state["last_material"], "material.md", "text/markdown")
    with col2:
        st.download_button("Download as Text", st.session_state["last_material"], "material.txt", "text/plain")
