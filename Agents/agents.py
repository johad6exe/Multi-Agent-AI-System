import os
#agno imports
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
#module imports
from RAG.knowledge import knowledge_base
from tracing.logger import sys_logger
from config import agent_model

# 1. The General Reasoning Agent
general_agent = Agent(
    name="General_Agent",
    model=agent_model,
    tools=[CalculatorTools(), DuckDuckGoTools(fixed_max_results=5, enable_news=False)],
    role="You are a brilliant multipurpose reasoning agent. You handle general inquiries, logic, and mathematics.",
    instructions=[
        "You must use the provided web search tool for any query asking for live, historical, or general knowledge data.",
        "You must use the provided calculator tool for all math queries involving calculations.",
        "For general conversations or facts, use your own knowledge."
    ],
    markdown=True
)

# 2. Optimized High-Speed Document Retriever Agent
retriever_agent = Agent(
    name="Retriever_Agent",
    model=agent_model,
    knowledge=knowledge_base,
    role="You are a meticulous RAG research assistant. You answer questions strictly using the given knowledge base.",
    instructions=[
        "Format the answer in a structured way for better readability.",
        "You are responsible for answering questions based ONLY on the provided knowledge base context.",
        "If the context does not contain the answer, state explicitly that the information is unavailable."
    ],
    search_knowledge=False,        # Stops the agent from running slow tool-use thinking loops
    add_knowledge_to_context=True,  # Automatically injects relevant context into the initial prompt
    markdown=True
)