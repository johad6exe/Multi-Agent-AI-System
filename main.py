import json
#module imports
from Agents.orchestrator import coordinator
from Agents.agents import general_agent, retriever_agent
from tracing.logger import sys_logger

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
            coordinator.print_response(user_query,stream = True)

        except KeyboardInterrupt:
            print("\nShutting down...")
            sys_logger.info("Process interrupted by user.")
            break
        except Exception as e:
            sys_logger.error(f"Runtime execution error: {str(e)}", exc_info=True)
            print(f"\nAn error occurred. Check the logs.")


if __name__ == "__main__":
    run_assistant()