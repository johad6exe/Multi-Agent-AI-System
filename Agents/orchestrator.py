# Agents/orchestrator.py
from agno.team import Team, TeamMode
from Agents.agents import retriever_agent, general_agent
from config import routing_model

# coordinator = Agent(
#     name="Coordinator",
#     model=routing_model,
#     role="You are a deterministic routing classifier for a multi-agent system.",
#     instructions=[
#         "Analyze the user's query and classify it into exactly and strictly one category: 'RETRIEVER' or 'GENERAL'.",
        
#         "CRITICAL RULE: At any case reply with ONLY the single word token ('RETRIEVER' or 'GENERAL'). Do not include markdown, punctuation, thinking, or extra text.",
        
#         "Route to 'RETRIEVER' if the query asks for financial results, metrics (like revenue, operating income), risks, disclosures, or statements regarding NVIDIA or MICROSOFT.",
        
#         "NOTE: Local 10-K filings cover FY2025, but they explicitly contain comparative historical metrics for prior years like FY2024 and FY2023. Route queries about NVIDIA/Microsoft financial history (FY23, FY24, FY25) to 'RETRIEVER'.",
        
#         "Route to 'GENERAL' for all other companies, general knowledge, real-time stock prices, math calculations, coding help, or general conversation.",
        
#         "Examples:",
#         "- 'Nvidia revenue in fiscal year 2024' -> RETRIEVER",
#         "- 'Microsoft risk factors disclosed' -> RETRIEVER",
#         "- 'What is Microsoft's current stock price right now?' -> GENERAL (requires real-time web search)",
#         "- 'Calculate compound interest' -> GENERAL (requires calculator tool)"
#     ]
# )

coordinator = Team(
    name="Coordinator_Team",
    model=routing_model, 
    members=[retriever_agent, general_agent],
    mode=TeamMode.route, 
    instructions=[
        "You are the team manager. Your only job is to analyze the user query and hand it off to the correct team member.",

        "Delegate to retriever_agent if the query asks for financial results, metrics (like revenue, operating income), risks, disclosures, or statements regarding NVIDIA or MICROSOFT from the years 2023-25.",
                
        "Route to 'GENERAL' for all other companies, general knowledge, real-time stock prices, math calculations, coding help, or general conversation.",
        
        "Examples:",
        "- 'Nvidia revenue in fiscal year 2024' -> RETRIEVER",
        "- 'Microsoft risk factors disclosed' -> RETRIEVER",
        "- 'What is Microsoft's current stock price right now?' -> GENERAL (requires real-time web search)",
        "- 'Calculate compound interest' -> GENERAL (requires calculator tool)"
    ],
    markdown=True
)