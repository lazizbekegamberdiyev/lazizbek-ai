from google import genai
from google.genai import types
from dotenv import load_dotenv

from tools.python_tool import run_python


load_dotenv()

client = genai.Client()


tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="run_python",
            description="Execute safe Python code for calculations and data analysis.",
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
        )
    ]
)


contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text="Use Python to calculate the mean of [10, 20, 30, 40, 50]."
            )
        ]
    )
]


response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=contents,
    config=types.GenerateContentConfig(tools=[tool])
)


function_call = None

for part in response.candidates[0].content.parts:
    if part.function_call:
        function_call = part.function_call
        break


if function_call:
    print("🔧 Tool called:", function_call.name)
    print("📥 Code:", function_call.args["code"])

    result = run_python(
        function_call.args["code"]
    )

    print("🐍 Python result:", result)

    contents.append(response.candidates[0].content)

    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part(
                    function_response=types.FunctionResponse(
                        name=function_call.name,
                        response={"result": result}
                    )
                )
            ]
        )
    )

    final_response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(tools=[tool])
    )

    print()
    print("🤖 Final AI response:")
    print(final_response.text)

else:
    print("❌ Gemini did not call Python Tool.")
    print(response.text)
