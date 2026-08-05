import streamlit as st
from utils.session import init_session_state, is_logged_in, get_username, set_login, logout
from utils.styles import apply_custom_styles, show_header
from utils.api_client import login

st.set_page_config(
    page_title="AI Teacher's Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
apply_custom_styles()

with st.sidebar:
    st.title("🎓 AI Teacher's Assistant")
    if is_logged_in():
        st.write(f"Welcome, **{get_username()}**!")
        if st.button("Logout"):
            logout()
            st.rerun()
    st.markdown("---")
    st.info("Use the pages above to navigate between features.")

if is_logged_in():
    show_header("Welcome Dashboard", f"Hello, {get_username()}! What would you like to create today?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Lesson Plans</h3>
            <p>Generate comprehensive, tailored lesson plans for any topic, subject, and grade level.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Quizzes</h3>
            <p>Create targeted quizzes based on your generated lesson plans instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Learning Materials</h3>
            <p>Design worksheets, notes, and handouts customized for your students.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Simplify Concepts</h3>
            <p>Get explanations for complex topics broken down for elementary, middle, and high school levels.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Classroom Activities</h3>
            <p>Generate engaging group activities, games, and discussions for your classes.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 Select a tool from the sidebar to get started.")

else:
    show_header("AI Teacher's Assistant", icon="🎓")
    st.markdown("Welcome! This tool helps educators quickly generate high-quality lesson plans, quizzes, and learning materials using advanced AI.")
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Login to Continue")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter any username to login")
                submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    if username.strip():
                        response = login(username.strip())
                        if response.get("success"):
                            set_login(response["data"]["username"])
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(response.get("message", "Login failed."))
                    else:
                        st.error("Please enter a username.")
