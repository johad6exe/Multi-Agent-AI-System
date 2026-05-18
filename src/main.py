from agno.agent import Agent
from src.agents import general_agent, retriever_agent, llm_model
from src.logger import sys_logger

# The Coordinator Agent
coordinator = Agent(
    name="Coordinator",
    model=llm_model,
    role="You are a strict, deterministic traffic router for a Multi-Agent system.",
    description=(
        "Analyze the user's query and classify it. Reply with EXACTLY ONE WORD:\n\n"
        "1. Reply 'RETRIEVER' ONLY if the user explicitly asks to search the knowledge base, or asks about historical documents like the GenAI Case Study, AWS EC2 manual, or Nvidia's PAST financial filings (e.g., 2024 revenue).\n"
        "2. Reply 'GENERAL' for ABSOLUTELY EVERYTHING ELSE. This explicitly includes: math equations, world trivia, greetings, AND requests for real-time data.\n\n"
        "CRITICAL RULE: Even if a keyword like 'Nvidia' is mentioned, if the user asks for CURRENT or LIVE data (like 'today's stock price' or 'recent news'), you MUST route to 'GENERAL' so it can search the web.\n\n"
        "Reply strictly with the single word 'RETRIEVER' or 'GENERAL'. No punctuation. No explanation."
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