import streamlit as st
import ollama
from duckduckgo_search import DDGS

st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")

# Sidebar
st.sidebar.title("🤖 My AI Assistant")
st.sidebar.write("Powered by Phi-3 + Web Search")
st.sidebar.write("Built using Streamlit & Ollama")

st.title("🌐 My AI Chatbot with Web Search")

# Clear chat button
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Web search function
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

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask anything..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            web_info = search_web(prompt)

            response = ollama.chat(
                model="phi3",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt + "\n\nWeb info:\n" + web_info}
                ]
            )

            reply = response["message"]["content"]

        st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
