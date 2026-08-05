import streamlit as st
from utils.session import init_session_state, require_login, is_generating, set_generating
from utils.styles import apply_custom_styles, show_header, show_model_badge
from utils.api_client import generate_quiz

st.set_page_config(page_title="Quiz Generator", page_icon="📝", layout="wide")
apply_custom_styles()
init_session_state()
require_login()

show_header("Quiz Generator", "Create quizzes based on your lesson plans", "📝")

if st.session_state.get("last_lesson_plan"):
    st.info("💡 Using the lesson plan you generated previously.")
    default_plan = st.session_state["last_lesson_plan"]
else:
    default_plan = ""

with st.form("quiz_form"):
    lesson_plan = st.text_area("Lesson Plan or Topic Details", value=default_plan, height=200, placeholder="Paste your lesson plan here...")
    num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)
    submit_button = st.form_submit_button("Generate Quiz", disabled=is_generating())

if submit_button:
    if not lesson_plan.strip():
        st.error("Please provide a lesson plan or topic details.")
    else:
        set_generating(True)
        with st.spinner("Generating quiz..."):
            response = generate_quiz(
                lesson_plan=lesson_plan.strip(), 
                num_questions=num_questions
            )
            
        set_generating(False)
        
        if response.get("success"):
            quiz = response["data"]["quiz"]
            st.session_state["last_quiz"] = quiz
            st.success("Quiz generated successfully!")
            show_model_badge(response.get("model_used", ""))
            
            st.markdown("### Generated Quiz")
            st.markdown(quiz)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download as Markdown", quiz, "quiz.md", "text/markdown")
            with col2:
                st.download_button("Download as Text", quiz, "quiz.txt", "text/plain")
        else:
            st.error(response.get("message", "Failed to generate quiz."))

elif st.session_state.get("last_quiz"):
    st.markdown("### Previous Quiz")
    st.markdown(st.session_state["last_quiz"])
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download as Markdown", st.session_state["last_quiz"], "quiz.md", "text/markdown")
    with col2:
        st.download_button("Download as Text", st.session_state["last_quiz"], "quiz.txt", "text/plain")
