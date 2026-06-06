# playground.py
from agno.os import AgentOS
# Import your actual instantiated agents
from Agents.orchestrator import coordinator

# Initialize the AgentOS runtime with your multi-agent workforce
agent_os = AgentOS(
    name="Research Multi-Agent System",
    teams=[coordinator]
)

# Generate the FastAPI application
app = agent_os.get_app()

if __name__ == "__main__":
    # Serve the AgentOS API locally on port 7777
    # Make sure the string matches your filename ("playground:app")
    agent_os.serve(app="playground:app", reload=True, port=7777)