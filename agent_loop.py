from agent import AgentState


MAX_STEPS = 5


def run_agent(goal):
    state = AgentState(goal)

    for step in range(MAX_STEPS):
        print(f"\\n🤖 Agent step {step + 1}")

        if state.final_answer:
            break

        action = "pending"

        state.add_action(action)

        print(f"🔧 Action: {action}")

        break

    return state


if __name__ == "__main__":
    state = run_agent("Calculate the average score")

    print("\\n🎯 Goal:", state.goal)
    print("🔧 Actions:", state.actions)
