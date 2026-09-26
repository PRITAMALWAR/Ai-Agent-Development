import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

# This loads the values from the .env file.
#
# .env contains:
#
# BASE_URL=http://localhost:11434/v1
# API_KEY=ollama
# MODEL=qwen3:1.7b

load_dotenv()


# ============================================================
# 2. READ CONFIGURATION
# ============================================================

# Read the values from .env

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")


# Check that configuration exists
if not BASE_URL:
    raise ValueError("BASE_URL is missing in .env")

if not API_KEY:
    raise ValueError("API_KEY is missing in .env")

if not MODEL:
    raise ValueError("MODEL is missing in .env")


# ============================================================
# 3. CREATE AI CLIENT
# ============================================================

# OpenAI's Python SDK is being used as the client.
#
# IMPORTANT:
# We are NOT sending the request to OpenAI's cloud.
#
# base_url points to our local Ollama server:
#
# http://localhost:11434/v1

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


# ============================================================
# 4. RESUME DATA
# ============================================================

# This is the resume text that we want the AI
# to convert into structured JSON.

resume_text = """
My name is Pritam Verma.

I am a Full Stack Developer.

I know React, Node.js, MongoDB, Python and PostgreSQL.

I am currently learning Generative AI.
"""


# ============================================================
# 5. CREATE PROMPT
# ============================================================

# We tell the AI exactly what information
# we want to extract.

prompt = f"""
Extract information from the resume text below.

Return ONLY valid JSON.

Do NOT use Markdown.
Do NOT use ```json.
Do NOT write any explanation.
Do NOT write anything before or after the JSON.

The JSON must contain exactly these fields:

name
role
skills
learning

Rules:

- name must be a string
- role must be a string
- skills must be an array of strings
- learning must be a string

Resume:

{resume_text}
"""


# ============================================================
# 6. SEND REQUEST TO AI
# ============================================================

print("Sending request to AI...")

response = client.chat.completions.create(
    model=MODEL,

    messages=[
        {
            "role": "system",
            "content": (
                "You are a resume information extraction assistant. "
                "Return only valid JSON."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    # We want deterministic output.
    temperature=0
)


# ============================================================
# 7. GET AI RESPONSE
# ============================================================

result = response.choices[0].message.content

print("\nRaw AI Response:")
print("----------------")
print(result)


# ============================================================
# 8. CLEAN AI RESPONSE
# ============================================================

# Some models may return:
#
# ```json
# {
#     ...
# }
# ```
#
# or:
#
# <think>...</think>
# {
#     ...
# }
#
# json.loads() cannot directly parse those.
#
# So we clean the response first.

clean_result = result.strip()


# Remove <think>...</think> if Qwen returns it.

if "<think>" in clean_result:

    think_end = clean_result.find("</think>")

    if think_end != -1:
        clean_result = clean_result[think_end + len("</think>"):].strip()


# Remove Markdown JSON code fences.

if clean_result.startswith("```json"):
    clean_result = clean_result[len("```json"):].strip()

if clean_result.startswith("```"):
    clean_result = clean_result[len("```"):].strip()

if clean_result.endswith("```"):
    clean_result = clean_result[:-3].strip()


# ============================================================
# 9. FIND JSON OBJECT
# ============================================================

# Find the first { and last }.
#
# This protects us if the model adds some extra text.

start = clean_result.find("{")
end = clean_result.rfind("}")


if start == -1 or end == -1:
    print("\nERROR: AI did not return valid JSON.")
    print("Cleaned response:")
    print(clean_result)
    exit()


json_text = clean_result[start:end + 1]


# ============================================================
# 10. CONVERT JSON STRING TO PYTHON DICTIONARY
# ============================================================

try:

    data = json.loads(json_text)

except json.JSONDecodeError as error:

    print("\nERROR: Could not parse AI response as JSON.")
    print("JSON Error:", error)

    print("\nResponse received from AI:")
    print(json_text)

    exit()


# ============================================================
# 11. DISPLAY PARSED JSON
# ============================================================

print("\nParsed JSON:")
print("------------")

print(
    json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )
)


# ============================================================
# 12. DISPLAY INDIVIDUAL VALUES
# ============================================================

print("\nExtracted Information:")
print("----------------------")


print("Name:", data.get("name"))

print("Role:", data.get("role"))

print("Skills:", data.get("skills"))

print("Learning:", data.get("learning"))