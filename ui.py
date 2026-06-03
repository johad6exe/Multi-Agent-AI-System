import streamlit as st
from Agents.agents import general_agent, retriever_agent
from Agents.orchestrator import coordinator

st.set_page_config(page_title="GenAI Multi-Agent System", page_icon="🤖")

st.title("🤖 Multi-Agent Research Assistant")
st.markdown("This system dynamically routes your query to the correct specialized Agent.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about Nvidia, AWS EC2, or general math..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Coordinator is analyzing intent..."):
        try:
            # 1. Get the route from the Coordinator
            route_response = coordinator.run(prompt)
            route = route_response.content.strip().upper()
            
            # 2. Hand off to the correct Worker Agent
            if "RETRIEVER" in route:
                st.info("🔄 Route: Delegating to Retriever Agent (RAG)")
                final_response = retriever_agent.run(prompt)
            else:
                st.info("🌐 Route: Delegating to General Agent (Web/Math)")
                final_response = general_agent.run(prompt)
            
            # 3. Display the final assistant response
            with st.chat_message("assistant"):
                st.markdown(final_response.content)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": final_response.content})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")