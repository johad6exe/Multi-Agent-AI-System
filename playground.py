from agno.os import AgentOS
# module imports
from Agents.orchestrator import coordinator

# Initializing the AgentOS runtime with multi-agent workforce
agent_os = AgentOS(
    name="Research Multi-Agent System",
    teams=[coordinator]
)

# FastAPI app
app = agent_os.get_app()

if __name__ == "__main__":
    #fastapi app serving at localhost:7777
    agent_os.serve(app="playground:app", reload=True, port=7777)