from tools.registry import get_tool


def execute_tool(name, arguments):
    tool = get_tool(name)

    if tool is None:
        return f"Unknown tool: {name}"

    try:
        return tool(**arguments)
    except Exception as e:
        return f"Tool execution error: {e}"
