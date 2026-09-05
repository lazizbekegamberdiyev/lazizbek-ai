from google import genai
from google.genai import types
from dotenv import load_dotenv
from tools.calculator_tool import calculator

load_dotenv()
client = genai.Client()

tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculator",
            description="Calculate a mathematical expression safely.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "expression": types.Schema(
                        type="STRING",
                        description="A mathematical expression."
                    )
                },
                required=["expression"],
            ),
        )
    ]
)

contents = [
    types.Content(
        role="user",
        parts=[types.Part(text="Calculate 15% of 2,000,000")]
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
    print("Tool called:", function_call.name)
    print("Arguments:", function_call.args)

    result = calculator(function_call.args["expression"])
    print("Tool result:", result)

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
    print("Final AI response:")
    print(final_response.text)

else:
    print("Gemini did not call the calculator tool.")
    print(response.text)
