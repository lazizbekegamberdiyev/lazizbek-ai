import json

from google import genai
from google.genai import types
from dotenv import load_dotenv

from agent_prompt import AGENT_SYSTEM_PROMPT
from agent_decision import parse_decision
from tools.declarations import TOOL

load_dotenv()

client = genai.Client()


def get_next_decision(goal, state):
    context = {
        "goal": goal,
        "actions": state.actions,
        "tool_results": state.tool_results,
    }

    prompt = f"""
{AGENT_SYSTEM_PROMPT}

CURRENT AGENT STATE:
{json.dumps(context, indent=2)}

USER GOAL:
{goal}

IMPORTANT RECOVERY RULE:

If the previous tool result has status "error":
- Analyze what went wrong.
- Do not repeat the exact same failed action.
- Choose another appropriate action if possible.
- If the task cannot be completed, return a final answer explaining the problem.

Decide what to do next.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[TOOL]
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_call = part.function_call

            return {
                "type": "tool",
                "name": function_call.name,
                "arguments": dict(function_call.args),
            }

    text = response.text.strip()

    return parse_decision(text)
