import streamlit as st
import os
import sys
import time
import re
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
        font-size: 2.2rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
        text-align: center;
    }
    
    .subtitle {
        color: #475569;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        text-align: center;
    }

    /* Suggestion Pills */
    .stButton>button {
        background-color: #ffffff;
        color: #00d09c;
        border: 1.5px solid #00d09c;
        border-radius: 50px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        height: auto;
        min-height: 3rem;
        white-space: normal;
        margin-bottom: 0.8rem;
        line-height: 1.2;
    }
    
    .stButton>button:hover {
        background-color: #00d09c;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0, 208, 156, 0.15);
        transform: translateY(-1px);
    }

    /* Chat Elements */
    [data-testid="stChatMessage"] {
        background-color: #f8fafc;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    [data-testid="stChatMessageContent"] p {
        color: #1e2232 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        margin-bottom: 0 !important;
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

    /* Footer / Disclaimer */
    .footer-container {
        text-align: center;
        padding: 2.5rem 0;
        margin-top: 4rem;
        border-top: 1px solid #f1f5f9;
    }
    .disclaimer-text {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .update-text {
        font-size: 0.75rem;
        color: #cbd5e1;
        margin-top: 0.6rem;
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

# Suggestions Logic
st.markdown('<p style="font-weight: 600; color: #334155; margin-bottom: 0.8rem; text-align:center;">Quick Suggestions</p>', unsafe_allow_html=True)
cols = st.columns(3)
suggestions = [
    "What is the expense ratio of Motilal Oswal Midcap Fund?",
    "What is the minimum SIP for Motilal Oswal Large and Midcap Fund?",
    "What is the exit load on Motilal Oswal ELSS Tax Saver Fund?"
]

selected_suggestion = None
for i, suggestion in enumerate(suggestions):
    if cols[i].button(suggestion, key=f"sug_{i}"):
        selected_suggestion = suggestion

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"]=="assistant" else "👤"):
        st.markdown(message["content"], unsafe_allow_html=True)

# Input handling
prompt = st.chat_input("Ask a factual question about mutual funds...")
if selected_suggestion:
    prompt = selected_suggestion

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing Groww records..."):
            response_text = st.session_state.chatbot.chat(prompt)
            
            # Formatting: Turn links into clickable HTML and handle newlines
            url_regex = r"(https?://[^\s]+)"
            formatted_response = re.sub(url_regex, r'<a href="\1" target="_blank" class="chat-link">\1</a>', response_text)
            formatted_response = formatted_response.replace("\n", "<br>")
            
            st.markdown(formatted_response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": formatted_response})
            
            # Streamlit rerun to finalize the view
            if selected_suggestion:
                st.rerun()

# Disclaimer
st.markdown(f"""
<div class="footer-container">
    <div class="disclaimer-text">FACTS-ONLY. NO INVESTMENT ADVICE.</div>
    <div class="update-text">System Knowledge Last Synchronized: {get_last_updated()}</div>
</div>
""", unsafe_allow_html=True)
