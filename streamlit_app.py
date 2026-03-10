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

# Custom CSS for Groww Branding
st.markdown("""
<style>
    :root {
        --groww-green: #00d09c;
        --groww-dark: #1e2232;
    }
    .stApp {
    .main {
        max-width: 800px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: var(--groww-dark) !important;
        font-weight: 700;
    }
    p, span, div.stMarkdown {
        color: var(--groww-dark) !important;
    }
    .stApp {
        background-color: white;
    }
    .stButton>button {
        background-color: white;
        color: var(--groww-green);
        border: 1px solid var(--groww-green);
        border-radius: 20px;
        padding: 5px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: var(--groww-green);
        color: white;
        border-color: var(--groww-green);
    }
    .chat-link {
        color: var(--groww-green);
        text-decoration: underline;
        font-weight: 500;
    }
    .disclaimer {
        font-size: 0.8rem;
        color: #64748b;
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #e2e8f0;
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
st.title("Groww FAQ Assistant")
st.write("Hello, welcome to Groww FAQ Assistant! 👋 How can I help you today?")

# Suggestions
st.write("### Try asking:")
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
        with st.spinner("Thinking..."):
            response_text = st.session_state.chatbot.chat(prompt)
            
            # Simple conversion of links to clickable HTML in markdown
            import re
            url_regex = r"(https?://[^\s]+)"
            formatted_response = re.sub(url_regex, r'<a href="\1" target="_blank" class="chat-link">\1</a>', response_text)
            formatted_response = formatted_response.replace("\n", "<br>")
            
            st.markdown(formatted_response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": formatted_response})
            # Force rerun to clear suggestion if used (Streamlit quirk)
            if selected_suggestion:
                st.rerun()

# Disclaimer
st.markdown(f"""
<div class="disclaimer">
    Facts-only. No investment advice.<br>
    Last updated from sources: {get_last_updated()}
</div>
""", unsafe_allow_html=True)
