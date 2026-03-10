import streamlit as st
import os
import sys
import time
from datetime import datetime

# Add project root to path to import chatbot
sys.path.append(os.path.dirname(__file__))
from phase_3_retrieval_generation.chatbot import GrowwChatbot

# Page configuration
st.set_page_config(
    page_title="Groww FAQ Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for Premium Groww branding
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff !important;
    }

    .main {
        max-width: 850px;
        margin: 0 auto;
    }

    /* Header Styling */
    h1 {
        color: #1e2232 !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
    }
    
    .subtitle {
        color: #475569;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Suggestion Pills */
    .stButton>button {
        background-color: #ffffff;
        color: #00d09c;
        border: 1.5px solid #00d09c;
        border-radius: 50px;
        padding: 0.4rem 1.2rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        height: auto;
        white-space: normal;
        margin-bottom: 0.5rem;
    }
    
    .stButton>button:hover {
        background-color: #00d09c;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0, 208, 156, 0.2);
        transform: translateY(-1px);
    }

    /* Chat Elements */
    [data-testid="stChatMessage"] {
        background-color: #f8fafc;
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }

    [data-testid="stChatMessageContent"] p {
        color: #1e2232 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }

    .chat-link {
        color: #00d09c;
        text-decoration: none;
        font-weight: 600;
        border-bottom: 1px solid transparent;
        transition: border-color 0.2s;
    }
    .chat-link:hover {
        border-bottom-color: #00d09c;
    }

    /* Input area */
    [data-testid="stChatInput"] {
        border-top: 1px solid #e2e8f0;
        background: white;
        padding-top: 1rem;
    }

    /* Footer / Disclaimer */
    .footer-container {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #f1f5f9;
    }
    .disclaimer-text {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
    }
    .update-text {
        font-size: 0.75rem;
        color: #cbd5e1;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = GrowwChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar/Footer Info
def get_last_updated():
    try:
        path = os.path.join(os.path.dirname(__file__), 'phase_4_frontend_backend', 'static', 'last_updated.txt')
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read().strip()
    except:
        pass
    return "2026-03-10"

# Header
st.markdown('<h1>Groww FAQ Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Hello, welcome to Groww FAQ Assistant! 👋 How can I help you today?</p>', unsafe_allow_html=True)

# Suggestions
st.markdown('<p style="font-weight: 600; color: #1e2232; margin-bottom: 0.5rem;">Try asking:</p>', unsafe_allow_html=True)
cols = st.columns(3)
# ... (rest of suggestions)
# ...
# Disclaimer
st.markdown(f"""
<div class="footer-container">
    <div class="disclaimer-text">Facts-only. No investment advice.</div>
    <div class="update-text">Last updated from sources: {get_last_updated()}</div>
</div>
""", unsafe_allow_html=True)
