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

Return the next decision as JSON.

If a tool is needed:
{{
    "type": "tool",
    "name": "tool_name",
    "arguments": {{}}
}}

If the task is complete:
{{
    "type": "final",
    "answer": "final answer"
}}

USER GOAL:
{goal}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[TOOL]
        ),
    )

    return parse_decision(response.text)
