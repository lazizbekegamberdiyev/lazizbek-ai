from google import genai
from google.genai import types
from dotenv import load_dotenv

from memory import init_db, load_memories
from prompt import SYSTEM_PROMPT

load_dotenv()

init_db()

client = genai.Client()

memories = load_memories()

memory_text = "\n".join(
    f"- {memory}" for memory in memories
)

if memory_text:
    FULL_SYSTEM_PROMPT = f"""
{SYSTEM_PROMPT}

LONG-TERM MEMORY ABOUT LAZIZBEK:

{memory_text}

Use these memories when they are relevant.
Do not mention the memory system unless Lazizbek asks about it.
"""
else:
    FULL_SYSTEM_PROMPT = SYSTEM_PROMPT


def handle_chat(user_input):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=FULL_SYSTEM_PROMPT
        )
    )

    return response.text
