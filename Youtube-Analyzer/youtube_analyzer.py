from textwrap import dedent
from os import getenv

from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.youtube import YouTubeTools

load_dotenv()


def build_agent():
    return Agent(
        name="YouTube Agent",

        model=OpenAILike(
            id="openai/gpt-oss-20b",
            api_key=getenv("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1",
        ),

        tools=[YouTubeTools()],

        instructions=dedent("""
            You are an expert YouTube content analyst with a keen eye for detail! 🎥

            Follow these steps for comprehensive video analysis:

            1. Video Overview
               - Check video length and basic metadata
               - Identify video type
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


def analyze_video(youtube_url):
    agent = build_agent()

    response = agent.run(
        f"Analyze this YouTube video: {youtube_url}"
    )

    return response.content