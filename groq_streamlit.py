import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import base64

load_dotenv("keys.env")

# ---- Page Config ----
st.set_page_config(page_title="Silvia's Chatbot", page_icon="🤖", layout="wide")

# ---- Function to load local image ----
def get_base64(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ---- Load your photo ----
img = get_base64("profile.jpeg")

# ---- Background + Profile Style ----
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&display=swap" rel="stylesheet">

    <style>

    /* ---- Full screen dark background ---- */
    html, body, [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stMainBlockContainer"],
    .stApp, .main, section.main > div {{
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460) !important;
        color: white !important;
    }}

    /* Remove white top bar */
    [data-testid="stHeader"] {{
        background: #1a1a2e !important;
    }}

    /* Remove white bottom bar */
    footer {{
        background: #1a1a2e !important;
    }}

    /* Profile picture - top right */
    .profile-container {{
        position: fixed;
        top: 60px;
        right: 20px;
        z-index: 999;
        text-align: center;
    }}
    .profile-container img {{
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 3px solid white;
        object-fit: cover;
    }}

    /* Title - centered, business font */
    h1 {{
        text-align: center;
        font-size: 2rem !important;
        color: white !important;
        font-family: 'Playfair Display', serif !important;
        letter-spacing: 2px;
    }}

    /* Remove chat bubble backgrounds */
    .stChatMessage {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* All chat text in white */
    .stChatMessage p {{
        color: white !important;
    }}

    /* Input box dark styling */
    [data-testid="stChatInput"] {{
        background-color: #16213e !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
    }}

    [data-testid="stChatInput"] textarea {{
        color: white !important;
        background-color: #16213e !important;
    }}

    </style>

    <div class="profile-container">
        <img src="data:image/jpeg;base64,{img}" alt="Creator"/>
    </div>
""", unsafe_allow_html=True)

# ---- App Title ----
st.title("Silvia's Chatbot")

# ---- Initialize session state ----
if "client" not in st.session_state:
    st.session_state.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# ---- Show welcome message on first load ----
if len(st.session_state.conversation) == 0:
    st.chat_message("assistant").write("Hello! What's on your mind today? 😊")

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