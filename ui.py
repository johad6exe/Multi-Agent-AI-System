import json
import streamlit as st
from Agents.agents import general_agent, retriever_agent
from Agents.orchestrator import coordinator

st.set_page_config(page_title="GenAI Multi-Agent System", page_icon="🤖")
st.title("🤖 Multi-Agent Research Assistant")
st.markdown("This system dynamically routes your query to the correct specialized Agent.")

# ── Session State ──────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Chat Input ─────────────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask about Nvidia, Microsoft, or general question..."):

    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            with st.spinner("Coordinator is analyzing intent..."):
                route_response = coordinator.run(prompt)
                final_response = route_response.content
                st.write(final_response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")