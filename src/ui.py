import uvicorn
from agno.os import AgentOS
from src.agents import general_agent, retriever_agent
from src.main import coordinator
from src.logger import sys_logger

# 1. Mount our agents to the AgentOS Runtime
agent_os = AgentOS(
    agents=[coordinator, general_agent, retriever_agent]
)

# Extract the FastAPI app instance
app = agent_os.get_app()

if __name__ == "__main__":
    sys_logger.info("Starting AgentOS local web dashboard on http://localhost:7777")
    # 2. Serve the application using standard Uvicorn
    uvicorn.run("src.ui:app", host="localhost", port=7777, reload=True)