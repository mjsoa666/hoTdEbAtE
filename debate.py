
import streamlit as st
import ollama
import random
import time
import os

# --- CONFIGURATION ---
MODEL_A = "brianmatzelle/llama3.1-8b-instruct-hasanpiker-abliterated:latest"
MODEL_B = "fellowtraveler/qwen4chan:latest"

# DISPLAY NAMES
NAME_A = "HasanAbi"
NAME_B = "Anon232347278343"

SYSTEM_PROMPT_A = (
    "You are Hasan Piker. You are a leftist, progressive streamer. "
    "You are debating a 4chan user. Speak in your style, be passionate, "
    "use twitch slang if needed. Keep responses concise (under 3 sentences)."
)

SYSTEM_PROMPT_B = (
    "You are an anonymous 4chan user (/pol/). You are debating a leftist streamer. "
    "Speak in greentext style or internet slang. Be edgy, skeptical, and contrarian. "
    "Keep responses concise (under 3 sentences)."
)

TOPICS = [
    "Universal Basic Income",
    "Gun Control Laws",
    "Capitalism vs Socialism",
    "Modern Immigration Policy",
    "Gender Identity Politics",
    "The role of the Police",
    "Crypto and NFTs"
]

st.set_page_config(page_title="AI Fight Club", layout="wide")
st.title(f"🤖 AI Debate Arena: {NAME_A} vs {NAME_B}")

# --- IMAGE DISPLAY ---
if os.path.exists("image.jpg"):
    st.image("image.jpg", width=600)
else:
    st.warning("⚠️ image.jpg not found. Place 'image.jpg' in the folder: " + os.getcwd())

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []
if "running" not in st.session_state:
    st.session_state.running = False
if "turn" not in st.session_state:
    st.session_state.turn = "A"

# --- SIDEBAR ---
with st.sidebar:
    st.header("Controls")
    if st.button("START DEBATE", type="primary"):
        st.session_state.running = True
        st.session_state.history = []
        topic = random.choice(TOPICS)
        st.session_state.history.append({"role": "system", "content": f"Topic: {topic}. BEGIN."})
        st.session_state.turn = "A"
        st.rerun()

    if st.button("STOP"):
        st.session_state.running = False
        st.rerun()

# --- CHAT HISTORY ---
for msg in st.session_state.history:
    if msg['role'] == "system":
        st.warning(msg['content'])
    elif msg.get('name') == NAME_A:
        with st.chat_message(NAME_A, avatar="🟥"):
            st.write(f"**{NAME_A}:** {msg['content']}")
    elif msg.get('name') == NAME_B:
        with st.chat_message(NAME_B, avatar="🟩"):
            st.write(f"**{NAME_B}:** {msg['content']}")

# --- DEBATE LOOP ---
if st.session_state.running:
    time.sleep(1) # Pacing
    try:
        if st.session_state.turn == "A":
            # HASAN'S TURN
            with st.chat_message(NAME_A, avatar="🟥"):
                with st.spinner(f"{NAME_A} is malding..."):
                    messages = [{'role': 'system', 'content': SYSTEM_PROMPT_A}]
                    for h in st.session_state.history[-8:]:
                        role = 'user' if h.get('name') == NAME_B else 'assistant'
                        if h['role'] == 'system': role = 'user'
                        messages.append({'role': role, 'content': h['content']})

                    response = ollama.chat(model=MODEL_A, messages=messages)
                    reply = response['message']['content']
                    st.write(f"**{NAME_A}:** {reply}")
            
            st.session_state.history.append({"role": "assistant", "name": NAME_A, "content": reply})
            st.session_state.turn = "B"
            st.rerun()

        elif st.session_state.turn == "B":
            # 4CHAN'S TURN
            with st.chat_message(NAME_B, avatar="🟩"):
                with st.spinner(f"{NAME_B} is typing..."):
                    messages = [{'role': 'system', 'content': SYSTEM_PROMPT_B}]
                    for h in st.session_state.history[-8:]:
                        role = 'user' if h.get('name') == NAME_A else 'assistant'
                        if h['role'] == 'system': role = 'user'
                        messages.append({'role': role, 'content': h['content']})

                    response = ollama.chat(model=MODEL_B, messages=messages)
                    reply = response['message']['content']
                    st.write(f"**{NAME_B}:** {reply}")

            st.session_state.history.append({"role": "assistant", "name": NAME_B, "content": reply})
            st.session_state.turn = "A"
            st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.running = False
