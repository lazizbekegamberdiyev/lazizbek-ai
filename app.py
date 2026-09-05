import streamlit as st

from router_brain import route_request
from router_executor import get_handler


st.set_page_config(
    page_title="Lazizbek AI",
    page_icon="🤖"
)

st.title("🤖 Lazizbek AI")
st.caption("Personal Data Science Copilot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("route"):
            st.caption(f"🚦 Route: {message['route']}")
        st.write(message["content"])

user_input = st.chat_input("Ask Lazizbek AI anything...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            decision = route_request(user_input)

            st.caption(f"🚦 Route: {decision.route}")

            handler = get_handler(decision)

            if decision.route == "chat":
                answer = handler(user_input)

            elif decision.route == "web":
                answer = handler(
                    user_input,
                    max_results=5
                )

            elif decision.route == "rag":
                answer = handler(
                    user_input,
                    n_results=3
                )

            elif decision.route == "tool":
                import re

                percentage_match = re.search(
                    r"(\d+(?:\.\d+)?)%\s+of\s+([\d,]+(?:\.\d+)?)",
                    user_input,
                    re.IGNORECASE
                )

                if percentage_match:
                    percentage = percentage_match.group(1)
                    number = percentage_match.group(2).replace(",", "")

                    expression = f"{percentage} * {number} / 100"

                    answer = handler(
                        "calculator",
                        {
                            "expression": expression
                        }
                    )
                else:
                    answer = (
                        "I can calculate simple expressions, "
                        "but I could not extract the mathematical expression."
                    )

            elif decision.route == "agent":
                answer = handler(user_input)

            else:
                answer = (
                    f"Router selected **{decision.route}** route. "
                    "This route will be connected next."
                )

            st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "route": decision.route
    })
