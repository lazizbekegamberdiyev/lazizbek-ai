from google import genai
from google.genai import types
from dotenv import load_dotenv

from tools.file_tool import read_file

load_dotenv()

client = genai.Client()

tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="read_file",
            description="Read the contents of an allowed file from the documents folder.",
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
        )
    ]
)

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text="Read students.csv and tell me how many students are in the file."
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
    print("📥 File:", function_call.args["filename"])

    result = read_file(function_call.args["filename"])

    print("📄 File result:")
    print(result)

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
    print("❌ Gemini did not call File Tool.")
    print(response.text)
