import os
#agno imports
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
#module imports
from RAG.knowledge import knowledge_base
from tracing.logger import sys_logger
from config import llm_model

# 1. The General Reasoning Agent
general_agent = Agent(
    name="General_Agent",
    model=llm_model,
    tools=[CalculatorTools(), DuckDuckGoTools(fixed_max_results=5, enable_news=False)],
    role="You are a brilliant multipurpose reasoning agent. You handle general inquiries, logic, and mathematics.",
    instructions=(f"You must use provided web search Tool {DuckDuckGoTools()} for any query asking for live, historical or General Knowledge data",
    f"You must use provided calculator tool {CalculatorTools()} for all math queries involving calculations",
    "for general conversations or facts use your own knowledge or if your knowledge is insufficient fall back to web search in this case too"),
    markdown=True
)

# 2. The Document Retriever Agent (Upgraded)
retriever_agent = Agent(
    name="Retriever_Agent",
    model=llm_model,
    knowledge=knowledge_base,
    role="You are a meticulous RAG research assistant. You answer questions strictly using the given knowledge base.",
    instructions=("Format the answer in a structured way for better readability","When you reply, you MUST append a 'SOURCES USED:' section at the bottom, citing the exact text chunks with text from the relevant chunks justifying your answer, AND the Cross-Encoder Relevance Scores provided by the tool."
    "You are responsible for answering questions based ONLY on the provided knowledge base context. If the context does not contain the answer, state explicitly that the information is unavailable in the documents."),
    search_knowledge = True,
    add_knowledge_to_context= False,
    markdown=True
)