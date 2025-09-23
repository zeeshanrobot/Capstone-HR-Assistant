import streamlit as st
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path="/home/notebooks/storage/.env")


## Fetching LLM text model  keys and deployment id from .env file:

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
DATAROBOT_KEY = os.getenv("DATAROBOT_KEY")
DEPLOYMENT_ID= os.getenv("DEPLOYMENT_ID")


# ----------------  *************************************Setting deployment and API credentials **************************************************
# -----------------------------
# ----------------------------DataRobot prediction function
# -----------------------------
class DataRobotPredictionError(Exception):
    pass

def make_datarobot_prediction(prompt: str) -> str:
    payload = [{"promptText": prompt}]
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "DataRobot-Key": DATAROBOT_KEY,
        "Content-Type": "application/json",
    }
    url = API_URL.format(deployment_id=DEPLOYMENT_ID)

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise DataRobotPredictionError(f"Error: {response.status_code} - {response.text}")

    prediction = response.json()["data"][0]["prediction"]
    return prediction


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="HR Assistant", page_icon="💬", layout="centered")

st.markdown("<h1>💬 Ask the HR Assistant</h1>", unsafe_allow_html=True)
st.markdown("This assistant answers your HR or onboarding-related questions using RAG-powered responses.")

# --- Session State for Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Clear Button ---
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# --- Chat Form ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask your question:")
    submit = st.form_submit_button("💬 Send")

# --- On submit ---
if submit and user_input.strip():
    try:
        with st.spinner("Thinking..."):
            response = make_datarobot_prediction(user_input)
        st.session_state.chat_history.append({
            "question": user_input,
            "answer": response
        })
    except Exception as e:
        st.error(f"❌ {e}")

# --- Display chat history (latest at bottom) ---
for chat in st.session_state.chat_history:
    st.markdown(f"🧑‍💼 **You:** {chat['question']}")
    st.markdown(f"🤖 **Assistant:** {chat['answer']}")
