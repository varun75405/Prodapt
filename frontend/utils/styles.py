import streamlit as st

def get_custom_css() -> str:
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Modern Color Scheme */
    :root {
        --primary-blue: #1E3A5F;
        --accent-gold: #F4A261;
        --light-bg: #F8F9FA;
        --card-bg: #FFFFFF;
        --text-dark: #2C3E50;
        --text-muted: #7F8C8D;
    }

    /* Styled sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A5F 0%, #152943 100%);
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Card-like containers */
    .stApp .block-container {
        padding-top: 2rem;
    }
    
    /* Styled buttons */
    .stButton > button {
        background-color: var(--primary-blue);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: var(--accent-gold);
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .stButton > button:disabled {
        background-color: var(--text-muted);
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }

    /* Download buttons */
    .stDownloadButton > button {
        background-color: var(--accent-gold);
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    .stDownloadButton > button:hover {
        background-color: #E76F51;
        color: white;
    }

    /* Form styling */
    div[data-testid="stForm"] {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #EAEAEA;
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
    }
    
    /* Feature Cards (Custom HTML) */
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-top: 4px solid var(--accent-gold);
        height: 100%;
        transition: transform 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-card h3 {
        color: var(--primary-blue);
        margin-top: 0;
    }
    """

def apply_custom_styles():
    st.markdown(f"<style>{get_custom_css()}</style>", unsafe_allow_html=True)

def show_header(title: str, subtitle: str = "", icon: str = ""):
    if icon:
        st.markdown(f"# {icon} {title}")
    else:
        st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.markdown("---")

def show_model_badge(model_used: str):
    if model_used:
        st.caption(f"🤖 Generated using: **{model_used}**")
