import json
import streamlit as st
from Agents.agents import general_agent, retriever_agent
from Agents.orchestrator import coordinator


# ── Shared Utility ─────────────────────────────────────────────────────────────
def extract_unique_chunks(response):
    """Extract and deduplicate chunks from all tool message calls."""
    all_chunks = []
    seen = set()

    for msg in response.messages:
        if msg.role == "tool" and isinstance(msg.content, str):
            # Skip explicit "no results" responses
            if msg.content.strip().lower() in ("no documents found", ""):
                continue
            try:
                chunks = json.loads(msg.content)
                if not isinstance(chunks, list):
                    continue
                for chunk in chunks:
                    meta = chunk.get("meta_data", {})
                    key = (chunk.get("name"), meta.get("page"), meta.get("chunk"))
                    if key not in seen:
                        seen.add(key)
                        all_chunks.append(chunk)
            except (json.JSONDecodeError, TypeError):
                continue

    return all_chunks


def render_chunks(chunks):
    """Render retrieved chunks inside an expander."""
    with st.expander(f"📚 Retrieved Chunks ({len(chunks)} unique)", expanded=False):
        for i, chunk in enumerate(chunks, 1):
            meta = chunk.get("meta_data", {})
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("File", chunk.get("name", "unknown"))
            col2.metric("Page", meta.get("page", "N/A"))
            col3.metric("Chunk #", meta.get("chunk", "N/A"))
            col4.metric("Size", f"{meta.get('chunk_size', 'N/A')} tokens")

            st.text_area(
                label=f"Content — Chunk {i}",
                value=chunk.get("content", ""),
                height=150,
                disabled=True,
                key=f"chunk_{i}_{meta.get('page')}_{meta.get('chunk')}_{id(chunks)}"
            )
            if i < len(chunks):
                st.divider()


# ── Page Config ────────────────────────────────────────────────────────────────

st.set_page_config(page_title="GenAI Multi-Agent System", page_icon="🤖")
st.title("🤖 Multi-Agent Research Assistant")
st.markdown("This system dynamically routes your query to the correct specialized Agent.")

# ── Session State ──────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render Chat History ────────────────────────────────────────────────────────

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Route badge (only on assistant messages that were routed)
        if message.get("route"):
            if "RETRIEVER" in message["route"]:
                st.info("🔄 Route: **Retriever Agent** (RAG)")
            else:
                st.info("🌐 Route: **General Agent** (Web/Math)")

        # Re-render chunks from history if present
        if message.get("chunks"):
            render_chunks(message["chunks"])

        st.markdown(message["content"])

# Temporary test button in ui.py
if st.button("🧪 Test LanceDB Direct"):
    from RAG.knowledge import knowledge_base
    results = knowledge_base.search("Nvidia revenue 2024")
    st.write(f"Direct search returned: {len(results)} docs")
    for r in results:
        st.write(r)

# ── Chat Input ─────────────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask about Nvidia, Microsoft, or general question..."):

    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # 1. Routing
            with st.spinner("Coordinator is analyzing intent..."):
                route_response = coordinator.run(prompt)
                route = route_response.content.strip().upper()

            # 2. Retriever path
            if "RETRIEVER" in route:
                st.info("🔄 Route: **Retriever Agent** (RAG)")

                with st.spinner("Searching knowledge base and generating answer..."):
                    final_response = retriever_agent.run(prompt, stream=False)
                
                debug_info = []
                for i, msg in enumerate(final_response.messages):
                     debug_info.append(f"[{i}] role={msg.role} | type(content)={type(msg.content).__name__} | content_preview={str(msg.content)[:100]}")
                st.code("\n".join(debug_info), language="text")

                unique_chunks = extract_unique_chunks(final_response)

                if unique_chunks:
                    render_chunks(unique_chunks)
                else:
                    st.warning("⚠️ No relevant documents found in the knowledge base for this query.")

                st.markdown(final_response.content)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_response.content,
                    "chunks": unique_chunks,
                    "route": route,
                })

            # 3. General path
            else:
                st.info("🌐 Route: **General Agent** (Web/Math)")

                with st.spinner("Processing..."):
                    final_response = general_agent.run(prompt, stream=False)

                st.markdown(final_response.content)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_response.content,
                    "route": route,
                })

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")