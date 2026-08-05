import streamlit as st

def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "logged_in": False,
        "username": "",
        "last_lesson_plan": None,
        "last_quiz": None,
        "last_material": None,
        "last_simplification": None,
        "last_activity": None,
        "generating": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)

def get_username() -> str:
    return st.session_state.get("username", "")

def set_login(username: str):
    st.session_state["logged_in"] = True
    st.session_state["username"] = username

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def require_login():
    """Check if user is logged in. If not, show warning and stop execution."""
    if not is_logged_in():
        st.warning("⚠️ Please log in first to access this feature.")
        st.info("👈 Go to the **Home** page to log in.")
        st.stop()

def set_generating(state: bool):
    st.session_state["generating"] = state

def is_generating() -> bool:
    return st.session_state.get("generating", False)
