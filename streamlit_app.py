import streamlit as st
import os
import sys
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(__file__))

from phase_3_retrieval_generation.chatbot import GrowwChatbot

# Configure Page
st.set_page_config(
    page_title="Groww FAQ Assistant",
    page_icon="🤖",
    layout="centered"
)

# Load CSS
css_path = os.path.join("phase_4_frontend_backend", "static", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        custom_css = f.read()
        st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# Additional Streamlit-specific overrides for better UI integration
st.markdown("""
<style>
    .stApp {
        background-color: #eef2f5;
    }
    .main .block-container {
        padding-top: 2rem;
        max-width: 450px;
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    footer {
        display: none;
    }
    [data-testid="stForm"] {
        border: none;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = GrowwChatbot()

# Initialize Chat History
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Header HTML
st.markdown("""
    <div class="chat-header">
        <div class="bot-info">
            <div class="bot-avatar">
                <img src="https://groww.in/logo-light-groww.ratul.svg" alt="Bot"
                    onerror="this.src='https://img.icons8.com/isometric/50/bot.png'">
                <span class="status-dot"></span>
            </div>
            <div class="bot-text">
                <h1 style='margin:0; padding:0; line-height:1;'>Groww ChatBot</h1>
                <span class="status-text">Online</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Chat messages container
st.markdown('<div class="chat-messages" id="chat-messages">', unsafe_allow_html=True)

# Helper to format response with links
def format_response(text):
    import re
    if not text: return ""
    url_regex = r'(https?://[^\s]+)'
    formatted = re.sub(url_regex, r'<a href="\1" target="_blank" class="chat-link" rel="noopener noreferrer">\1</a>', text)
    return formatted.replace('\n', '<br>')

# Initial Welcome Messages
if not st.session_state.messages:
    welcome_messages = [
        {"role": "bot", "content": "Hello, welcome to Groww FAQ Assistant! 👋"},
        {"role": "bot", "content": "How can I help you today?"}
    ]
    for msg in welcome_messages:
        st.session_state.messages.append(msg)

# Display Messages
for msg in st.session_state.messages:
    role = msg["role"]
    content = format_response(msg["content"])
    avatar_symbol = "🤖" if role == "bot" else "👤"
    
    st.markdown(f"""
        <div class="message {role}">
            <div class="avatar-small">{avatar_symbol}</div>
            <div class="message-content">
                <p>{content}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Last Updated Timestamp
last_updated_path = os.path.join("phase_4_frontend_backend", "static", "last_updated.txt")
last_updated_text = ""
if os.path.exists(last_updated_path):
    with open(last_updated_path, "r") as f:
        last_updated_text = f.read().strip()

# Footer / Suggestions
if len(st.session_state.messages) <= 2:
    st.markdown("""
        <div class="suggestion-chips" style="padding-left: 40px; margin-bottom: 20px;">
            <p style="font-size: 12px; color: #7c7e8c; margin-bottom: 8px;">Try asking:</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    
    suggestions = [
        "What is the expense ratio of Motilal Oswal Midcap Fund?",
        "What is the minimum SIP for Motilal Oswal Large and Midcap Fund?",
        "What is the exit load on Motilal Oswal ELSS Tax Saver Fund?"
    ]
    
    if col1.button("📈 Expense Ratio"):
        prompt = suggestions[0]
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("🤖 Thinking..."):
            response = st.session_state.chatbot.chat(prompt)
            st.session_state.messages.append({"role": "bot", "content": response})
        st.rerun()
        
    if col2.button("💰 Minimum SIP"):
        prompt = suggestions[1]
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("🤖 Thinking..."):
            response = st.session_state.chatbot.chat(prompt)
            st.session_state.messages.append({"role": "bot", "content": response})
        st.rerun()

    if col3.button("🔒 Exit Load"):
        prompt = suggestions[2]
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("🤖 Thinking..."):
            response = st.session_state.chatbot.chat(prompt)
            st.session_state.messages.append({"role": "bot", "content": response})
        st.rerun()

st.markdown(f"""
    <div class="disclaimer">Facts-only. No investment advice. Last updated: {last_updated_text}</div>
""", unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Send a message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("🤖 Thinking..."):
        response = st.session_state.chatbot.chat(prompt)
        st.session_state.messages.append({"role": "bot", "content": response})
    
    st.rerun()
