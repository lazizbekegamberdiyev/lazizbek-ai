import json


def parse_decision(text):
    try:
        decision = json.loads(text)

        if not isinstance(decision, dict):
            raise ValueError("Decision must be an object.")

        decision_type = decision.get("type")

        if decision_type == "tool":
            if not decision.get("name"):
                raise ValueError("Tool name is missing.")

            return {
                "type": "tool",
                "name": decision["name"],
                "arguments": decision.get("arguments", {})
            }

        if decision_type == "final":
            return {
                "type": "final",
                "answer": decision.get("answer", "")
            }

        raise ValueError("Unknown decision type.")

    except json.JSONDecodeError as e:
        return {
            "type": "error",
            "message": f"Invalid JSON: {e}"
        }

    except ValueError as e:
        return {
            "type": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    test = '{"type": "tool", "name": "read_file", "arguments": {"filename": "students.csv"}}'

    print("🧠 Raw decision:")
    print(test)

    print("\n✅ Parsed decision:")
    print(parse_decision(test))
