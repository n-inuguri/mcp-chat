# streamlit_app.py

import streamlit as st
from agent import run_agent

st.set_page_config(page_title="MCP Chatbot", page_icon="🤖")

st.title("MCP Chatbot")

st.write("Ask me anything about products, customers, or orders.")

if "history" not in st.session_state:
    st.session_state.history = []

# Chat history display
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)

# User input box (friendly natural language)
user_input = st.chat_input("Type your question...")

if user_input:
    # Show user message
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    # Run agent
    with st.chat_message("assistant"):
        response = run_agent(user_input)
        st.write(response)

    st.session_state.history.append(("assistant", response))