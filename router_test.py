from router_brain import route_request
from router_executor import get_handler


user_input = "Calculate 15% of 2,000,000."

print("👤 User:")
print(user_input)

print("\n🧠 Router:")
decision = route_request(user_input)
print(decision)

handler = get_handler(decision)

print("\n🚦 Selected handler:")
print(handler.__name__)

if decision.route == "tool":
    result = handler(
        "calculator",
        {
            "expression": "15 * 2000000 / 100"
        }
    )
else:
    result = handler(user_input)

print("\n📤 Result:")
print(result)
