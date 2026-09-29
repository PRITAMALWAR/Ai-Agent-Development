from agno.agent import Agent
from agno.models.ollama import Ollama

from dotenv import load_dotenv

load_dotenv()


def build_agent():
    return Agent(
        model=Ollama(
            id="qwen3:1.7b",
            host="http://localhost:11434"
        ),
        markdown=True,
        instructions="You are a helpful and expert travel agent."
    )


ollama_agent = build_agent()

ollama_agent.print_response(
    "My budget is 1 INR, should I travel to Goa or Phuket?"
)