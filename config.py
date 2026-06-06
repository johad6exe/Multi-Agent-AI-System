import os
#.env imports
from dotenv import load_dotenv
#agno imports
from agno.models.openrouter import OpenRouter
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.models.groq import Groq
# from agno.knowledge.reranker.cohere import CohereReranker
#module imports
from tracing.logger import sys_logger

load_dotenv()

ROUTING_KEY = os.getenv("GROQ_API")
AGENT_KEY = os.getenv("OPENROUTER_API_KEY")
if not AGENT_KEY and ROUTING_KEY:
    sys_logger.critical("API key for LLM call is missing from your .env file!")

ROUTING_MODEL = "llama-3.1-8b-instant"
LLM_MODEL = "google/gemini-2.5-flash-lite"
EMBG_MODEL = "nvidia/llama-nemotron-embed-vl-1b-v2:free"

agent_model = OpenRouter(
    id=LLM_MODEL,
    api_key= AGENT_KEY
)

routing_model = Groq(
    id=ROUTING_MODEL,
    api_key= ROUTING_KEY)

embedder = OpenAIEmbedder(
    id="nvidia/llama-nemotron-embed-vl-1b-v2:free",
    api_key=AGENT_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# reranker = CohereReranker(
#     model="cohere/rerank-4-pro",
#     api_key=LLM_KEY,
#     top_n=5
# )

