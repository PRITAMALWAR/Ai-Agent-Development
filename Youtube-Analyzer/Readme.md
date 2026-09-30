- 1. Create a virtual environment

python3 -m venv .venv
sudo apt install python3-venv


- 2. Activate it

source .venv/bin/activate


- 3. Upgrade pip

python -m pip install --upgrade pip


- 4. Install your packages

pip install agno streamlit openai groq ddgs


- 5. Then run your agent

python agent.py




======== Diploy Our Project ==============

website  = streamlit.io

python -m pip install streamlit agno openai python-dotenv youtube-transcript-api

- run ui.py

streamlit run ui.py















from textwrap import dedent

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.youtube import YouTubeTools

youtube_agent = Agent(
    name="YouTube Agent",
    model=Ollama(id="qwen3:1.7b"),
    tools=[YouTubeTools()],
    instructions=dedent("""
        You are an expert YouTube content analyst with a keen eye for detail! 
        Follow these steps for comprehensive video analysis:

        1. Video Overview
           - Check video length and basic metadata
           - Identify video type (tutorial, review, lecture, etc.)
           - Note the content structure

        2. Timestamp Creation
           - Create precise, meaningful timestamps
           - Focus on major topic transitions
           - Highlight key moments and demonstrations
           - Format: [start_time, end_time, detailed_summary]

        3. Content Organization
           - Group related segments
           - Identify main themes
           - Track topic progression

        Your analysis style:
        - Begin with a video overview
        - Use clear, descriptive segment titles
        - Include relevant emojis for content types:
            Educational
            Technical
            Gaming
            Tech Review
            Creative
        - Highlight key learning points
        - Note practical demonstrations
        - Mark important references

        Quality Guidelines:
        - Verify timestamp accuracy
        - Avoid timestamp hallucination
        - Ensure comprehensive coverage
        - Maintain consistent detail level
        - Focus on valuable content markers
    """),
    add_datetime_to_context=True,
    markdown=True,
)

youtube_agent.print_response(
    "Analyze this video: https://youtu.be/yGB9jhsEsr8?si=x7VVT0fjGaJTAemM",
    stream=True,
)