from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

model = os.getenv("MODEL")

# Conversation memory
messages = []

print("=" * 50)
print("              My AI Assistant")
print("=" * 50)
print("Type 'exit' to quit.\n")

while True:

    question = input("You : ")

    if question.lower() in ["exit", "quit", "bye"]:
        print("AI  : Goodbye!")
        break

    # Store user message
    messages.append({
        "role": "user",
        "content": question
    })

    # Send conversation history
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # Get AI response
    answer = response.choices[0].message.content

    # Store AI response
    messages.append({
        "role": "assistant",
        "content": answer
    })

    print("\nAI  :", answer)
    print()