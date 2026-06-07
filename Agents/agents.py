import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.calculator import CalculatorTools
#module imports
from RAG.knowledge import knowledge_base
from tracing.logger import sys_logger
from config import LLM, TAVILY_KEY
    
# 1. The General Reasoning Agent
general_agent = Agent(
    name="General_Agent",
    model=LLM,
    tools=[CalculatorTools(), TavilyTools(api_key=TAVILY_KEY,search_depth = "basic")],
    role="You are a brilliant multipurpose reasoning agent. You handle general inquiries, logic, and math calculations.",
    instructions=[
        "Always do include a heading GENERAL AGENT at the beginning of the answer.",
        "You must use the provided web search tool for any query asking for live, historical, or general knowledge data.",
        "You must use the provided calculator tool for all math queries involving calculations.",
        "For general conversations or facts, use your own knowledge."
    ],
    markdown=True
)

# 2. Optimized High-Speed Document Retriever Agent
retriever_agent = Agent(
    name="Retriever_Agent",
    model=LLM,
    knowledge=knowledge_base,
    role="You are a meticulous RAG research assistant. You answer questions strictly using the given knowledge base.",
    instructions=[
        "Always do include a heading RETRIEVER AGENT at the beginning of the answer.",
        "Format the answer in a structured way for better readability.",
        "You are responsible for answering questions based ONLY on the provided knowledge base context.",
        "CRITICAL : If the context does not contain the answer, state explicitly that the information is unavailable.",
        # rules for source chunks & citing
        "CRITICAL : After your answer, add a section: '📚 Evidence & Sources'.",
        "For each chunk used, create a block using this exact structure:",
        "Document: [Name] | Page: [X]",
        "> [2-3 line Summarized snippet of the specific information used from this chunk]",
        # "Ensure there is a double line break between each document block.",
        # Guardrails
        "Do not dump raw, unformatted chunks.",
        "Do not output any raw JSON or metadata syntax.",
        "If you use multiple pages from the same document, group them together under one heading.",
        "Maintain a clean, polished layout that renders well in Markdown."
    ],
    search_knowledge=False,        
    add_knowledge_to_context=True, # injects context into the model prompt
    markdown=True
)