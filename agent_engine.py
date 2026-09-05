from agent import AgentState
from agent_brain import get_next_decision
from agent_executor import execute_decision


MAX_STEPS = 5


def run_agent(goal):
    state = AgentState(goal)

    for step in range(1, MAX_STEPS + 1):
        print(f"\n🤖 Agent Step {step}")

        decision = get_next_decision(
            goal,
            state
        )

        print(f"🧠 Decision: {decision}")

        if decision["type"] == "error":
            print("❌ Agent error:", decision["message"])
            break

        result = execute_decision(
            state,
            decision
        )

        if decision["type"] == "tool":
            print(f"📤 Tool result: {result}")

        elif decision["type"] == "final":
            print(f"🤖 Final Answer: {result}")
            break

    return state
