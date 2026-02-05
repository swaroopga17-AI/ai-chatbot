import streamlit as st
import requests
from duckduckgo_search import DDGS

st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")

st.sidebar.title("🤖 My AI Assistant")
st.sidebar.write("Powered by Free Cloud AI + Web Search")

st.title("🌐 My AI Chatbot")

if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

def search_web(query):
    results_text = ""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            for r in results:
                results_text += r.get("body", "") + "\n"
    except:
        results_text = "No web results found."
    return results_text

def query_hf(prompt):
    API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]["generated_text"]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            web_info = search_web(prompt)
            full_prompt = f"{prompt}\n\nWeb info:\n{web_info}"
            reply = query_hf(full_prompt)

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
