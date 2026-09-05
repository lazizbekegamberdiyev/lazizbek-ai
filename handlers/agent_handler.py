from agent_engine import run_agent


def handle_agent(user_input):
    state = run_agent(user_input)

    if state.final_answer:
        return state.final_answer

    return "The agent could not complete the task."


if __name__ == "__main__":
    result = handle_agent(
        "Read students.csv and calculate the average score."
    )

    print("🤖 Agent Handler:")
    print(result)
