import re
import json

from google import genai
from google.genai import types
from dotenv import load_dotenv

from router import create_decision

load_dotenv()

client = genai.Client()


ROUTER_PROMPT = """
You are the Router of Lazizbek AI.

Your job is to classify the user's request into exactly ONE route.

AVAILABLE ROUTES:

- chat:
  General conversation, explanations, learning questions, or questions
  that do not require external tools or current information.

- web:
  Questions requiring current, recent, external, or live information
  from the internet.

- rag:
  Questions specifically about documents uploaded to Lazizbek AI.

- tool:
  Tasks that can be solved by one specific tool, such as a simple
  calculation.

- agent:
  Complex tasks requiring multiple steps, multiple tools, file analysis,
  or sequential decision-making.

ROUTING RULES:

1. Choose exactly one route.
2. Prefer "rag" when the user asks about uploaded documents.
3. Prefer "web" when current or external information is required.
4. Prefer "tool" for a simple single-tool task.
5. Prefer "agent" when multiple steps or multiple tools are required.
6. Use "chat" for normal conversation and explanations.
7. Do not execute any tools.
8. Do not answer the user's question.
9. Return ONLY valid JSON.

OUTPUT FORMAT:

{
    "route": "chat",
    "reason": "Short explanation"
}

The route must be exactly one of:
chat, web, rag, tool, agent.
"""


chat = client.chats.create(
    model="gemini-3.5-flash"
)


def route_request(user_input):
    prompt = f"""
{ROUTER_PROMPT}

USER REQUEST:
{user_input}
"""

    response = chat.send_message(
        message=prompt
    )

    response_text = (response.text or "").strip()

    if not response_text:
        raise ValueError(
            "Router received an empty response from Gemini."
        )

    # Gemini may return JSON inside Markdown code fences.
    response_text = re.sub(
        r"^```(?:json)?\\s*|\\s*```$",
        "",
        response_text,
        flags=re.IGNORECASE
    ).strip()

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Router received invalid JSON: {response_text!r}"
        ) from e

    if "route" not in data:
        raise ValueError(
            f"Router response does not contain a route: {data}"
        )

    return create_decision(
        data["route"],
        data.get("reason", "")
    )


if __name__ == "__main__":
    test_questions = [
        "What is a Python list?",
        "What is today's USD exchange rate?",
        "What is panel data in my lecture?",
        "Calculate 15% of 2,000,000.",
        "Read students.csv and calculate the average score.",
    ]

    print("🧠 Testing Router Brain...\n")

    for question in test_questions:
        decision = route_request(question)

        print(f"❓ {question}")
        print(f"➡️  {decision}")
        print()
