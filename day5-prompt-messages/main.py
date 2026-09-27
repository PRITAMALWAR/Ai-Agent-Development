import os

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# DAY 5
# SYSTEM / USER / ASSISTANT MESSAGES
# + PROMPT TEMPLATES
# ============================================================


# ============================================================
# 1. LOAD .env FILE
# ============================================================

# load_dotenv() reads the values from our .env file.
#
# Our .env contains:
#
# BASE_URL=http://localhost:11434/v1
# API_KEY=ollama
# MODEL=qwen3:1.7b
#
# This keeps configuration separate from our Python code.

load_dotenv()


# ============================================================
# 2. GET CONFIGURATION
# ============================================================

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")


# Make sure required configuration exists.

if not BASE_URL:
    raise ValueError("BASE_URL is missing from .env")

if not API_KEY:
    raise ValueError("API_KEY is missing from .env")

if not MODEL:
    raise ValueError("MODEL is missing from .env")


# ============================================================
# 3. CREATE AI CLIENT
# ============================================================

# OpenAI SDK is being used as the Python client.
#
# IMPORTANT:
#
# We are connecting to LOCAL OLLAMA,
# not OpenAI's cloud API.
#
# BASE_URL points to:
#
# http://localhost:11434/v1

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


# ============================================================
# 4. SYSTEM MESSAGE
# ============================================================

# The system message defines the AI's behavior.
#
# It tells the model:
#
# "Who are you?"
# "How should you behave?"
# "What style should you use?"
#
# The user does not normally provide this instruction.

system_message = """
You are a helpful technical tutor.

Your job is to explain programming and
Generative AI concepts to beginners.

Follow these rules:

1. Explain concepts in simple language.
2. Give practical examples.
3. Use short sections.
4. If code is required, provide Python code.
5. Do not make the explanation unnecessarily complicated.
"""


# ============================================================
# 5. PROMPT TEMPLATE
# ============================================================

# A prompt template is a reusable prompt.
#
# Instead of writing a completely new prompt every time,
# we create a template containing variables.
#
# {topic}
# {question}
#
# Python will replace these variables later.

prompt_template = """
I am learning Generative AI.

Topic:
{topic}

Question:
{question}

Please explain the answer for a beginner.

Use this structure:

1. Simple explanation
2. Why it is important
3. Practical example
4. Python example if useful
"""


# ============================================================
# 6. FUNCTION TO ASK AI
# ============================================================

def ask_ai(topic, question):
    """
    Send a question to the AI using:
    
    SYSTEM message
    USER message
    
    The prompt template is filled using the
    topic and question provided by the user.
    """

    # --------------------------------------------------------
    # Fill the prompt template
    # --------------------------------------------------------

    user_prompt = prompt_template.format(
        topic=topic,
        question=question
    )


    # --------------------------------------------------------
    # Send messages to the AI
    # --------------------------------------------------------

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.2
    )


    # --------------------------------------------------------
    # Get AI's answer
    # --------------------------------------------------------

    answer = response.choices[0].message.content

    return answer


# ============================================================
# 7. DISPLAY APPLICATION HEADER
# ============================================================

print("=" * 60)
print("             DAY 5 - AI TUTOR")
print("=" * 60)

print()


# ============================================================
# 8. INTERACTIVE LOOP
# ============================================================

while True:

    # Ask the user for the topic.

    topic = input("Topic : ").strip()


    # Allow user to exit.

    if topic.lower() == "exit":
        print("Goodbye!")
        break


    # Ask the user for their question.

    question = input("Question : ").strip()


    # Allow user to exit.

    if question.lower() == "exit":
        print("Goodbye!")
        break


    print()
    print("AI is thinking...")
    print()


    # --------------------------------------------------------
    # Call our function
    # --------------------------------------------------------

    try:

        answer = ask_ai(
            topic,
            question
        )

        print("=" * 60)
        print("AI ANSWER")
        print("=" * 60)
        print()

        print(answer)

        print()
        print("=" * 60)
        print()

    except Exception as error:

        print()
        print("Something went wrong:")
        print(error)
        print()