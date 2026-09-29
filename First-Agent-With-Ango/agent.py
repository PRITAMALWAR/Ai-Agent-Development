from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.ollama import Ollama

load_dotenv()

ollama_agent = Agent(
    model=Ollama(
        id="qwen3:1.7b",
        host="http://localhost:11434"
    ),
    markdown=True
)

ollama_agent.print_response(
    "Explain what an AI agent is.",
    stream=True
)