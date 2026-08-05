import streamlit as st
from utils.session import init_session_state, require_login, is_generating, set_generating
from utils.styles import apply_custom_styles, show_header, show_model_badge
from utils.api_client import simplify_concept

st.set_page_config(page_title="Simplify Concept", page_icon="🔍", layout="wide")
apply_custom_styles()
init_session_state()
require_login()

show_header("Simplify Complex Concepts", "Get explanations tailored for different grade levels", "🔍")

with st.form("simplify_form"):
    concept = st.text_input("Concept to Simplify", max_chars=200, placeholder="e.g., Quantum Mechanics, The Electoral College")
    subject_display = st.selectbox("Subject", ["Math", "Science", "English", "History", "Art", "General"])
    subject_map = {"Math": "math", "Science": "science", "English": "english", "History": "history", "Art": "art", "General": "general"}
    
    submit_button = st.form_submit_button("Simplify Concept", disabled=is_generating())

if submit_button:
    if not concept.strip():
        st.error("Please enter a concept.")
    else:
        set_generating(True)
        with st.spinner("Simplifying concept..."):
            response = simplify_concept(
                concept=concept.strip(), 
                subject=subject_map[subject_display]
            )
            
        set_generating(False)
        
        if response.get("success"):
            explanations = response["data"]["explanations"]
            st.session_state["last_simplification"] = explanations
            st.success("Concept simplified successfully!")
            show_model_badge(response.get("model_used", ""))
            
            tab1, tab2, tab3 = st.tabs(["🟢 Elementary", "🟡 Middle School", "🔴 High School"])
            
            with tab1:
                st.markdown(explanations["elementary"])
            with tab2:
                st.markdown(explanations["middle"])
            with tab3:
                st.markdown(explanations["high"])
                
            combined_content = f"# {concept}\n\n## Elementary Level\n{explanations['elementary']}\n\n## Middle School Level\n{explanations['middle']}\n\n## High School Level\n{explanations['high']}"
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download All as Markdown", combined_content, "simplified_concept.md", "text/markdown")
            with col2:
                st.download_button("Download All as Text", combined_content, "simplified_concept.txt", "text/plain")
        else:
            st.error(response.get("message", "Failed to simplify concept."))

elif st.session_state.get("last_simplification"):
    explanations = st.session_state["last_simplification"]
    
    tab1, tab2, tab3 = st.tabs(["🟢 Elementary", "🟡 Middle School", "🔴 High School"])
    with tab1:
        st.markdown(explanations["elementary"])
    with tab2:
        st.markdown(explanations["middle"])
    with tab3:
        st.markdown(explanations["high"])
        
    combined_content = f"# Previous Concept\n\n## Elementary Level\n{explanations['elementary']}\n\n## Middle School Level\n{explanations['middle']}\n\n## High School Level\n{explanations['high']}"
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download All as Markdown", combined_content, "simplified_concept.md", "text/markdown")
    with col2:
        st.download_button("Download All as Text", combined_content, "simplified_concept.txt", "text/plain")
