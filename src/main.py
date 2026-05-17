from agno.agent import Agent
from src.agents import general_agent, retriever_agent, llm_model
from src.logger import sys_logger

# The Coordinator Agent
coordinator = Agent(
    name="Coordinator",
    model=llm_model,
    role="You are a smart traffic router for a Multi-Agent system.",
    description=(
        "Analyze the user's query and reply with exactly ONE word indicating the target agent:\n"
        "1. Reply 'RETRIEVER' if the user asks about uploaded files, AWS EC2, the Case Study, Nvidia financials, or specific document facts.\n"
        "2. Reply 'GENERAL' if the user asks for math calculations, web searches, or general conversational logic.\n"
        "Reply strictly with the single word. No punctuation. No explanation."
    )
)

def run_assistant():
    sys_logger.info("Starting Multi-Agent System Engine...")
    
    print("\n" + "="*60)
    print("🤖 Multi-Agent Research Assistant Initialized")
    print("   (Type 'exit' to quit)")
    print("="*60 + "\n")
    
    while True:
        try:
            user_query = input("\nUser: ")
            if user_query.lower() in ['exit', 'quit']:
                sys_logger.info("Received exit command. Shutting down.")
                break
                
            if not user_query.strip():
                continue

            # 1. Routing Phase (Classification)
            sys_logger.info("Coordinator is analyzing intent...")
            decision_response = coordinator.run(user_query)
            route = decision_response.content.strip().upper()
            
            # 2. Execution Phase
            print(f"\n[System Route] -> Delegating to {route} AGENT...")
            
            if "RETRIEVER" in route:
                # print_response automatically streams the output to the CLI
                retriever_agent.print_response(user_query, stream=True)
                
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