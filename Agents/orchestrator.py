from agno.team import Team, TeamMode
#module imports
from Agents.agents import retriever_agent, general_agent
from config import LLM

coordinator = Team(
    name="Coordinator_Team",
    model=LLM, 
    members=[retriever_agent, general_agent],
    mode=TeamMode.route, 
    instructions=[
        "You are the team manager. Your only job is to analyze the user query and hand it off to the correct team member.",

        "Delegate to retriever_agent only if the query asks for financial metrics, risks, disclosures, or statements regarding NVIDIA or MICROSOFT from the years 2023-25.",
                
        "Route to 'GENERAL' for all other queries of general knowledge, real-time stock prices, math calculations, coding help, or general conversation.",
        
        "Examples:",
        "- 'Nvidia revenue in fiscal year 2024' -> RETRIEVER, because revenue is straight reference to 10K filings within 2023-25",
        "- 'Microsoft risk factors disclosed' -> RETRIEVER, because risk factors are present in 10K filings",
        "- 'What is Microsoft's current stock price right now?' -> GENERAL (requires real-time web search)",
        "- 'Calculate compound interest' -> GENERAL (requires calculator tool)"
    ],
    markdown=True
)