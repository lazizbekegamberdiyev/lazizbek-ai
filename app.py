import streamlit as st
from pathlib import Path

from router_brain import route_request
from router_executor import get_handler
from rag import search_documents


st.set_page_config(
    page_title="Lazizbek AI",
    page_icon="🤖"
)

with st.sidebar:
    st.header("🤖 Lazizbek AI")
    st.caption("Personal Data Science Copilot")
    
    st.divider()
    
    st.subheader("System")

    if "active_panel" not in st.session_state:
        st.session_state.active_panel = None

    status_items = [
        ("🧠", "Memory"),
        ("📚", "Documents / RAG"),
        ("🌐", "Web Search"),
        ("🔧", "Tools"),
        ("🤖", "Agent"),
        ("🚦", "Router"),
    ]

    for icon, name in status_items:
        if st.button(
            f"{icon} {name}  • Online",
            key=f"panel_{name}",
            use_container_width=True
        ):
            st.session_state.active_panel = name

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Model: Gemini 3.5 Flash")
    st.caption("Version: V11 • UI")

st.title("🤖 Lazizbek AI")
st.caption("Personal Data Science Copilot")

# Module information panels
if st.session_state.active_panel:
    panel = st.session_state.active_panel

    if panel == "Memory":
        from memory import load_memories, get_memory_count

        memories = load_memories()

        st.info("🧠 **Long-Term Memory**")
        st.metric("Stored memories", get_memory_count())

        if memories:
            for memory in memories:
                st.write(f"• {memory}")
        else:
            st.write("No long-term memories stored yet.")

    elif panel == "Documents / RAG":
        documents_path = Path("documents")
        documents = [
            file.name
            for file in documents_path.iterdir()
            if file.is_file()
        ] if documents_path.exists() else []

        st.info("📚 **Documents / RAG**")
        if documents:
            st.write("Available documents:")
            for document in documents:
                st.write(f"• {document}")
        else:
            st.write("No documents uploaded.")

    elif panel == "Web Search":
        from web_search import search_web

        st.info("🌐 **Web Search**")
        st.write(
            "Uses DuckDuckGo search to retrieve current "
            "external information."
        )

        try:
            test_results = search_web(
                "Python data science",
                max_results=3
            )

            st.metric("Search results available", len(test_results))

            if test_results:
                st.write("Example results:")
                for result in test_results:
                    st.write(f"• {result['title']}")
        except Exception as e:
            st.warning(f"Web search unavailable: {e}")

    elif panel == "Tools":
        from tools.registry import TOOLS

        st.info("🔧 **Tools**")
        st.write("Available tools in the system:")

        for tool_name in TOOLS:
            st.write(f"• `{tool_name}`")

        st.metric("Registered tools", len(TOOLS))

    elif panel == "Agent":
        from agent_engine import MAX_STEPS

        st.info("🤖 **Agent**")
        st.write(
            "The autonomous agent can plan multiple steps, "
            "use tools and execute tasks toward a final answer."
        )

        st.metric("Maximum steps per task", MAX_STEPS)

        st.write("Capabilities:")
        st.write("• 🧠 Planning")
        st.write("• 🔧 Tool execution")
        st.write("• 🔄 Multi-step workflow")
        st.write("• ✅ Final answer generation")

    elif panel == "Router":
        from router import VALID_ROUTES

        st.info("🚦 **Router**")
        st.write(
            "The router analyzes each request and selects "
            "the most appropriate processing route."
        )

        st.metric("Available routes", len(VALID_ROUTES))

        st.write("Routes:")
        route_icons = {
            "chat": "💬",
            "web": "🌐",
            "rag": "📚",
            "tool": "🔧",
            "agent": "🤖",
        }

        for route in sorted(VALID_ROUTES):
            st.write(f"{route_icons.get(route, '🚦')} `{route}`")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("route"):
            route_icons = {
                "chat": "💬",
                "web": "🌐",
                "rag": "📚",
                "tool": "🔧",
                "agent": "🤖",
                "error": "⚠️"
            }

            route = message["route"]
            icon = route_icons.get(route, "🚦")

            st.caption(f"{icon} {route.upper()}")
        st.write(message["content"])

        if message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"**{source['source']} — Page {source['page']}**"
                    )

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

            try:
                decision = route_request(user_input)
            except Exception as e:
                error_text = str(e)

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    answer = "⚠️ Gemini API quota has been reached. Please try again later."
                elif "503" in error_text or "UNAVAILABLE" in error_text:
                    answer = "⚠️ Gemini is temporarily unavailable. Please try again later."
                else:
                    answer = f"⚠️ Something went wrong: {error_text}"

                st.error(answer)
                st.stop()

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
                rag_results = search_documents(
                    user_input,
                    n_results=3
                )

                if rag_results:
                    answer_parts = []

                    for result in rag_results:
                        answer_parts.append(
                            result["text"]
                        )

                    answer = "\n\n".join(answer_parts)
                else:
                    answer = (
                        "The uploaded documents do not contain "
                        "enough relevant information."
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

            if decision.route == "rag" and rag_results:
                with st.expander("📚 Sources"):
                    for result in rag_results:
                        st.markdown(
                            f"**{result['source']} — Page {result['page']}**"
                        )

            assistant_message = {
                "role": "assistant",
                "content": answer,
                "route": decision.route
            }

            if decision.route == "rag" and rag_results:
                assistant_message["sources"] = [
                    {
                        "source": result["source"],
                        "page": result["page"]
                    }
                    for result in rag_results
                ]

            st.session_state.messages.append(assistant_message)
