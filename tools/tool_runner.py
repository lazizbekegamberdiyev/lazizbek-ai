from google.genai import types

from tools.executor import execute_tool


def run_tool_loop(chat, response):
    while True:
        function_call = None

        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call = part.function_call
                break

        if not function_call:
            return response

        tool_name = function_call.name
        tool_arguments = dict(function_call.args)

        print()
        print(f"🔧 Tool called: {tool_name}")
        print(f"📥 Arguments: {tool_arguments}")

        tool_result = execute_tool(
            tool_name,
            tool_arguments
        )

        print("📤 Tool result:")
        print(tool_result)

        response = chat.send_message(
            message=types.Part(
                function_response=types.FunctionResponse(
                    name=tool_name,
                    response={"result": tool_result}
                )
            )
        )
