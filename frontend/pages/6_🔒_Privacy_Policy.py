import streamlit as st
import os
from utils.styles import apply_custom_styles, show_header

st.set_page_config(page_title="Privacy Policy", page_icon="🔒", layout="wide")
apply_custom_styles()

show_header("Privacy Policy", "How we handle your data", "🔒")

# Load privacy policy markdown file
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "privacy_policy.md")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        privacy_policy_content = f.read()
    st.markdown(privacy_policy_content)
except FileNotFoundError:
    st.error("Privacy Policy document not found.")
