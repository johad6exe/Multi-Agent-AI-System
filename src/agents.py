import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from src.tools import evaluate_math_expression, real_web_search, advanced_rag_search
from src.logger import sys_logger

load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    sys_logger.critical("OPENROUTER_API_KEY is missing from your .env file!")


llm_model = OpenRouter(
    id=os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet"),
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 1. The General Reasoning Agent
general_agent = Agent(
    name="General_Agent",
    model=llm_model,
    role="You are a brilliant analytical assistant. You handle general inquiries, logic, and mathematics.",
    tools=[evaluate_math_expression, real_web_search],
    markdown=True
)

# 2. The Document Retriever Agent (Upgraded)
retriever_agent = Agent(
    name="Retriever_Agent",
    model=llm_model,
    role="You are a meticulous research assistant. You answer questions strictly using your advanced search tool.",
    # FIX: We pass our custom reranking tool directly to the agent
    tools=[advanced_rag_search],
    # FIX: We update the prompt to instruct the agent to output the Relevance Scores
    description=(
        "You must use the 'advanced_rag_search' tool to find answers in the knowledge base."
        "When you reply, you MUST append a 'SOURCES USED:' section at the bottom, citing the exact text chunks with text from the relevant chunks justifying your answer, AND the Cross-Encoder Relevance Scores provided by the tool."
        "You are responsible for answering questions based ONLY on the provided knowledge base context. If the context does not contain the answer, state explicitly that the information is unavailable in the documents."
    ),
    markdown=True
)

sys_logger.info("Workers (General_Agent, Retriever_Agent) instantiated successfully.")