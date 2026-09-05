class RouterDecision:
    def __init__(self, route, reason=""):
        self.route = route
        self.reason = reason

    def __repr__(self):
        return f"RouterDecision(route={self.route!r}, reason={self.reason!r})"


VALID_ROUTES = {
    "chat",
    "web",
    "rag",
    "tool",
    "agent",
}


def create_decision(route, reason=""):
    if route not in VALID_ROUTES:
        raise ValueError(f"Invalid route: {route}")

    return RouterDecision(
        route=route,
        reason=reason
    )


if __name__ == "__main__":
    test_routes = [
        ("chat", "General conversation"),
        ("web", "Requires current information"),
        ("rag", "Question about uploaded documents"),
        ("tool", "Requires a specific tool"),
        ("agent", "Requires multiple steps"),
    ]

    print("🧠 Testing Router routes...\n")

    for route, reason in test_routes:
        decision = create_decision(route, reason)
        print(f"✅ {decision}")

    print("\n🎯 All Router routes are valid!")
