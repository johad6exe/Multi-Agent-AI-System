import os
#.env imports
from dotenv import load_dotenv
#agno imports
from agno.models.openrouter import OpenRouter
#module imports
from tracing.logger import sys_logger

load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    sys_logger.critical("OPENROUTER_API_KEY is missing from your .env file!")

llm_model = OpenRouter(
    id=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY")
)

