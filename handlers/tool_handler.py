from tools.executor import execute_tool


def handle_tool(tool_name, arguments):
    return execute_tool(
        tool_name,
        arguments
    )


if __name__ == "__main__":
    result = handle_tool(
        "calculator",
        {
            "expression": "(85 + 92 + 78) / 3"
        }
    )

    print("🔧 Tool Handler:")
    print(result)
