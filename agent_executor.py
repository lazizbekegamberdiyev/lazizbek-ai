from agent import AgentState
from tools.executor import execute_tool


def execute_decision(state, decision):
    if decision["type"] == "tool":
        tool_name = decision["name"]
        arguments = decision.get("arguments", {})

        state.add_action({
            "type": "tool",
            "name": tool_name,
            "arguments": arguments
        })

        result = execute_tool(
            tool_name,
            arguments
        )

        result_text = str(result)

        is_error = (
            result_text.startswith("Error:")
            or result_text.startswith("Security Error:")
            or result_text.startswith("Syntax Error:")
            or result_text.startswith("Tool execution error:")
            or result_text.startswith("File not found:")
            or result_text.startswith("Unsupported file type:")
        )

        state.add_tool_result({
            "tool": tool_name,
            "result": result_text,
            "status": "error" if is_error else "success"
        })

        return result_text

    if decision["type"] == "final":
        answer = decision.get("answer", "")
        state.set_final_answer(answer)
        return answer

    return f"Unknown decision type: {decision.get('type')}"
