from agno.agent import Agent
from agno.models.ollama import Ollama

from dotenv import load_dotenv

load_dotenv()


def build_agent():
    return Agent(
        model=Ollama(id="qwen3:1.7b"),
        markdown=True,
        instructions="You are a helpful and expert travel agent."
    )


agent = build_agent()

agent.print_response("My budget is 1L INR, should I travel to Goa or Phuket?")