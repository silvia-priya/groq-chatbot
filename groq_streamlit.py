import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import base64

load_dotenv("keys.env")

# ---- Page Config ----
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="wide")

# ---- Function to load local image ----
def get_base64(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ---- Load your photo ----
img = get_base64("profile.jpeg")

# ---- Background + Profile Style ----
st.markdown(f"""
    <style>
    /* Background */
    .stApp {{
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: white;
    }}

    /* Profile picture - bigger */
    .profile-container {{
        position: fixed;
        top: 60px;
        left: 15px;
        z-index: 999;
        text-align: center;
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        width: 100px;
    }}
    .profile-container img {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 2px solid #00d4ff;
        object-fit: cover;
    }}
    .profile-container p {{
        color: #000000;
        font-size: 12px;
        margin-top: 6px;
        font-weight: bold;
    }}

    /* Title in center */
    h1 {{
        text-align: center;
        font-size: 1.8rem !important;
        color: white !important;
    }}

    /* Remove chat bubble background colors */
    .stChatMessage {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* All chat text in white */
    .stChatMessage p {{
        color: white !important;
    }}

    </style>

    <div class="profile-container">
        <img src="data:image/jpeg;base64,{img}" alt="Creator"/>
        <p>Made by<br/>Silvia Priya</p>
    </div>
""", unsafe_allow_html=True)

# ---- App Title ----
st.title("Silvia's Chatbot")

# ---- Initialize session state ----
if "client" not in st.session_state:
    st.session_state.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
if "conversation" not in st.session_state:
    st.session_state.conversation = []

SYSTEM_MSG = """You are a helpful Q&A assistant.
Answer questions clearly and concisely.
If you don't know, say so honestly."""

# ---- Display chat history ----
for msg in st.session_state.conversation:
    st.chat_message(msg["role"]).write(msg["content"])

# ---- Input box ----
if prompt := st.chat_input("Ask anything..."):
    st.session_state.conversation.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = st.session_state.client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            *st.session_state.conversation
        ]
    )

    reply = response.choices[0].message.content
    st.session_state.conversation.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)