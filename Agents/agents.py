import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from RAG.knowledge import knowledge_base
from tracing.logger import sys_logger

load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    sys_logger.critical("OPENROUTER_API_KEY is missing from your .env file!")

llm_model = OpenRouter(
    id=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 1. The General Reasoning Agent
general_agent = Agent(
    name="General_Agent",
    model=llm_model,
    tools=[CalculatorTools(), DuckDuckGoTools(fixed_max_results=5, enable_news=False)],
    role="You are a brilliant analytical assistant. You handle general inquiries, logic, and mathematics.",
    instructions="You must use given tools to answer questions.",
    markdown=True
)

# 2. The Document Retriever Agent (Upgraded)
retriever_agent = Agent(
    name="Retriever_Agent",
    model=llm_model,
    knowledge=knowledge_base,
    role="You are a meticulous research assistant. You answer questions strictly using the given knowledge base.",
    instructions=("When you reply, you MUST append a 'SOURCES USED:' section at the bottom, citing the exact text chunks with text from the relevant chunks justifying your answer, AND the Cross-Encoder Relevance Scores provided by the tool."
    "You are responsible for answering questions based ONLY on the provided knowledge base context. If the context does not contain the answer, state explicitly that the information is unavailable in the documents."),
    search_knowledge = True,
    add_knowledge_to_context= True,
    markdown=True
)