import os
from dotenv import load_dotenv
#agno imports
from agno.models.openrouter import OpenRouter
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.reranker.cohere import CohereReranker
#module imports
from tracing.logger import sys_logger

load_dotenv()

if not (LLM_KEY := os.getenv("OPENROUTER_API_KEY")):
    sys_logger.critical("Openrouter api key is missing from your .env file!")
    raise RuntimeError("API key required!")

if not (TAVILY_KEY := os.getenv("TAVILY_KEY")):
    sys_logger.critical("Tavily API key is missing from your .env file!!")
    raise RuntimeError("API key required!")

if not (COHERE_API_KEY := os.getenv("COHERE_API_KEY")):
    sys_logger.critical("Cohere API key is missing from your .env file!!")
    raise RuntimeError("API key required!")

# LLM_MODEL = "google/gemini-2.5-flash-lite"
LLM_MODEL = "openai/gpt-oss-120b:nitro"
EMBG_MODEL = "nvidia/llama-nemotron-embed-vl-1b-v2:free"

LLM = OpenRouter(
    id=LLM_MODEL,
    api_key= LLM_KEY
)

embedder = OpenAIEmbedder(
    id="qwen/qwen3-embedding-8b",
    api_key=LLM_KEY,
    base_url="https://openrouter.ai/api/v1"
)

reranker = CohereReranker(
    model="rerank-multilingual-v3.0",
    api_key = COHERE_API_KEY,
    top_n = 5
)

