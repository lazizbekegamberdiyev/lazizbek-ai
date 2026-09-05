from google import genai
from google.genai import types
from dotenv import load_dotenv

from tools.registry import TOOLS

load_dotenv()

client = genai.Client()

tool_declarations = [
    types.FunctionDeclaration(
        name="calculator",
        description="Calculate a mathematical expression safely.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "expression": types.Schema(
                    type="STRING",
                    description="Mathematical expression to calculate."
                )
            },
            required=["expression"],
        ),
    ),
    types.FunctionDeclaration(
        name="run_python",
        description="Execute restricted Python code for calculations and data analysis.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "code": types.Schema(
                    type="STRING",
                    description="Python code to execute."
                )
            },
            required=["code"],
        ),
    ),
    types.FunctionDeclaration(
        name="read_file",
        description="Read an allowed file from the documents folder.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "filename": types.Schema(
                    type="STRING",
                    description="Name of the file to read."
                )
            },
            required=["filename"],
        ),
    ),
]

tool = types.Tool(function_declarations=tool_declarations)

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text="Read students.csv and calculate the average score of the students."
            )
        ],
    )
]

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=contents,
    config=types.GenerateContentConfig(tools=[tool]),
)

for part in response.candidates[0].content.parts:
    if part.function_call:
        function_call = part.function_call

        print("🔧 Tool called:", function_call.name)
        print("📥 Arguments:", dict(function_call.args))

        if function_call.name == "read_file":
            result = TOOLS["read_file"](
                function_call.args["filename"]
            )

        elif function_call.name == "calculator":
            result = TOOLS["calculator"](
                function_call.args["expression"]
            )

        elif function_call.name == "run_python":
            result = TOOLS["run_python"](
                function_call.args["code"]
            )

        else:
            result = "Unknown tool."

        print("📤 Tool result:")
        print(result)
