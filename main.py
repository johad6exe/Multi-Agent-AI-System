import json
#module imports
from Agents.orchestrator import coordinator
from Agents.agents import general_agent, retriever_agent
from tracing.logger import sys_logger

def extract_unique_chunks(response):
    """Extract chunks cleanly from Agno's pre-retrieved context."""
    all_chunks = []
    # If the framework attached references directly to the response object
    if hasattr(response, 'context_data') and response.context_data:
        # Access pre-retrieved chunks safely depending on framework versions
        return response.context_data
    
    # Fallback parser for standard message evaluation
    seen = set()
    if hasattr(response, 'messages'):
        for msg in response.messages:
            if msg.role == "tool" and isinstance(msg.content, str):
                try:
                    chunks = json.loads(msg.content)
                    if not isinstance(chunks, list): continue
                    for chunk in chunks:
                        meta = chunk.get("meta_data", {})
                        key = (chunk.get("name"), meta.get("page"), meta.get("chunk"))
                        if key not in seen:
                            seen.add(key)
                            all_chunks.append(chunk)
                except Exception:
                    continue
    return all_chunks


def run_assistant():
    sys_logger.info("Starting Multi-Agent System Engine...")

    print("\n" + "=" * 60)
    print("🤖 Multi-Agent Research Assistant Initialized")
    print("   (Type 'exit' to quit)")
    print("=" * 60 + "\n")

    while True:
        try:
            user_query = input("\nUser: ")
            if user_query.lower() in ["exit", "quit"]:
                sys_logger.info("Received exit command. Shutting down.")
                break

            if not user_query.strip():
                continue

            # 1. Routing Phase
            sys_logger.info("Coordinator is analyzing intent...")
            decision_response = coordinator.run(user_query)
            route = decision_response.content.strip().upper()

            # 2. Execution Phase
            print(f"\n[System Route] -> Delegating to {route} AGENT...")

            if "RETRIEVER" in route:
                retriever_agent.print_response(user_query, stream=True)
                # response = retriever_agent.run(user_query, stream=False)

                # # ── Retrieved Chunks ───────────────────────────────────
                # unique_chunks = extract_unique_chunks(response)

                # print("\n" + "=" * 60)
                # print(f"📚 RETRIEVED CHUNKS ({len(unique_chunks)} unique)")
                # print("=" * 60)

                # if unique_chunks:
                #     for i, chunk in enumerate(unique_chunks, 1):
                #         meta = chunk.get("meta_data", {})
                #         content = chunk.get("content", "")
                #         name = chunk.get("name", "unknown")

                #         print(f"\n── Chunk {i} {'─' * 44}")
                #         print(f"  📄 File    : {name}")
                #         print(f"  📃 Page    : {meta.get('page', 'N/A')}")
                #         print(f"  🔢 Chunk # : {meta.get('chunk', 'N/A')}")
                #         print(f"  📏 Size    : {meta.get('chunk_size', 'N/A')} tokens")
                #         print(f"\n  📝 Content :\n  {content}")
                # else:
                #     print("\n  ⚠️  No chunks retrieved from knowledge base.")

                # # ── Final Answer ───────────────────────────────────────
                # print("\n" + "=" * 60)
                # print("💬 AGENT RESPONSE")
                # print("=" * 60)
                # print(f"\n{response.content}\n")

            else:
                general_agent.print_response(user_query, stream=True)

        except KeyboardInterrupt:
            print("\nShutting down...")
            sys_logger.info("Process interrupted by user.")
            break
        except Exception as e:
            sys_logger.error(f"Runtime execution error: {str(e)}", exc_info=True)
            print(f"\nAn error occurred. Check the logs.")


if __name__ == "__main__":
    run_assistant()