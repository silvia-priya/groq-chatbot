import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

st.title("🤖 Groq Chatbot")

# Initialize everything inside session state
if "client" not in st.session_state:
    #st.session_state.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    st.session_state.client = Groq(api_key="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")
if "conversation" not in st.session_state:
    st.session_state.conversation = []

SYSTEM_MSG = """You are a helpful Q&A assistant.
Answer questions clearly and concisely.
If you don't know, say so honestly."""

# Display chat history
for msg in st.session_state.conversation:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box
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