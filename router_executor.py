from router import RouterDecision

from handlers.chat_handler import handle_chat
from handlers.web_handler import handle_web
from handlers.rag_handler import handle_rag
from handlers.tool_handler import handle_tool
from handlers.agent_handler import handle_agent


ROUTE_HANDLERS = {
    "chat": handle_chat,
    "web": handle_web,
    "rag": handle_rag,
    "tool": handle_tool,
    "agent": handle_agent,
}


def get_handler(decision):
    if not isinstance(decision, RouterDecision):
        raise TypeError("Expected a RouterDecision.")

    handler = ROUTE_HANDLERS.get(decision.route)

    if handler is None:
        raise ValueError(
            f"No handler registered for route: {decision.route}"
        )

    return handler


if __name__ == "__main__":
    print("🚦 Testing Router Executor...\n")

    test_routes = [
        "chat",
        "web",
        "rag",
        "tool",
        "agent",
    ]

    for route in test_routes:
        decision = RouterDecision(
            route,
            f"Testing {route} route"
        )

        handler = get_handler(decision)

        print(
            f"✅ {route} → {handler.__name__}"
        )

    print("\n🎯 All routes connected to real handlers!")
