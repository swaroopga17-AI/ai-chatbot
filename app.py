import streamlit as st
import requests
import os

# --- HuggingFace API Setup ---
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

# Fetch token from Streamlit Secrets or Environment Variables
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    except Exception as e:
        return f"❌ Connection error: {e}"

    # If API failed
    if response.status_code != 200:
        return f"❌ API Error {response.status_code}: {response.text}"

    try:
        result = response.json()
    except:
        return "❌ Failed to read AI response."

    # If HuggingFace sends error message
    if isinstance(result, dict) and "error" in result:
        return f"⚠️ HuggingFace Error: {result['error']}"

    # If valid answer comes
    if isinstance(result, list) and len(result) > 0:
        if "generated_text" in result[0]:
            return result[0]["generated_text"]

    # Fallback
    return "⚠️ Unexpected response format from AI."

# --- Streamlit User Interface ---
st.set_page_config(page_title="My Personal AI Assistant", page_icon="🤖")

# Sidebar
with st.sidebar:
    st.header("🎛️ Controls")
    st.markdown("🎤 **Voice Input**")
    st.button("Click to Talk")
    
    st.divider()
    
    st.header("🎭 Personality")
    style = st.selectbox("Choose Style:", ["Helpful Assistant 🤓"])
    
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# Main Title
st.title("🎙️ My Personal AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type something..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and show AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = query_hf(prompt)
            st.markdown(response_text)
            
    # Save assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
