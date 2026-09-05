from google import genai
from google.genai import types
from dotenv import load_dotenv

from memory import (
    init_db,
    save_message,
    load_messages,
    save_memory,
    load_memories
)

from prompt import SYSTEM_PROMPT
from web_search import search_web
from rag import search_documents


load_dotenv()

init_db()

client = genai.Client()


# -----------------------------------
# Load conversation history
# -----------------------------------

saved_messages = load_messages()

history = []

for role, content in saved_messages:
    history.append(
        types.Content(
            role=role,
            parts=[
                types.Part(text=content)
            ]
        )
    )


# -----------------------------------
# Load long-term memories
# -----------------------------------

memories = load_memories()

memory_text = "\n".join(
    f"- {memory}" for memory in memories
)

if memory_text:
    full_system_prompt = f"""
{SYSTEM_PROMPT}

LONG-TERM MEMORY ABOUT LAZIZBEK:

{memory_text}

Use these memories when they are relevant.
Do not mention the memory system unless Lazizbek asks about it.
"""
else:
    full_system_prompt = SYSTEM_PROMPT


# -----------------------------------
# Create Gemini chat
# -----------------------------------

chat = client.chats.create(
    model="gemini-3.5-flash",
    history=history,
    config=types.GenerateContentConfig(
        system_instruction=full_system_prompt
    )
)


print("🤖 Lazizbek AI ishga tushdi!")
print("🧠 Memory: ON")
print("💾 Permanent Memory: ON")
print("⭐ Long-Term Memory: ON")
print("🎭 Personality: ON")
print("🌐 Free Web Search: ON")
print("Chiqish uchun: exit")
print()


# -----------------------------------
# Main chat
# -----------------------------------

while True:

    try:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Lazizbek AI: Goodbye! 👋")
            break

        if not user_input:
            continue


        # -----------------------------------
        # Web Search
        # -----------------------------------

        search_results = search_web(user_input, max_results=5)

        web_context = ""

        if search_results:
            web_context = "\n\n".join(
                f"TITLE: {result['title']}\n"
                f"URL: {result['href']}\n"
                f"INFO: {result['body']}"
                for result in search_results
            )


        # -----------------------------------
        # Document RAG Search
        # -----------------------------------
        document_results = search_documents(user_input, n_results=3)
        document_context = ""

        if document_results:
            document_context = "\n\n".join(
                f"SOURCE: {result['source']} | PAGE: {result['page']}\n"
                f"CONTENT: {result['text']}"
                for result in document_results
            )

        # -----------------------------------
        # Send message to Gemini
        # -----------------------------------

        message = f"""
You are Lazizbek AI.

Answer the user's question using the provided context.

IMPORTANT RULES:
- For questions about the uploaded documents, use ONLY the DOCUMENT CONTEXT.
- Do not add facts, examples, theories, or explanations that are not supported by the DOCUMENT CONTEXT.
- Preserve the terminology and meaning used in the document.
- If the DOCUMENT CONTEXT does not contain enough information, say:
  "The uploaded document does not provide enough information to answer this."
- Do not use general knowledge to fill missing information.
- WEB SEARCH CONTEXT may be used only when the question requires current or external information.
- Keep document-based answers faithful to the uploaded material.

DOCUMENT CONTEXT:
{document_context if document_context else "No relevant document context found."}

WEB SEARCH CONTEXT:
{web_context if web_context else "No web search results found."}

USER QUESTION:
{user_input}
"""

        save_message("user", user_input)

        response = chat.send_message(
            message=message
        )

        ai_text = response.text

        save_message("model", ai_text)

        print()
        print("AI:", ai_text)

        if document_results:
            print()
            print("📚 Sources:")

            seen_sources = set()

            for result in document_results:
                source_key = (result["source"], result["page"])

                if source_key not in seen_sources:
                    print(
                        f"- {result['source']} — Page {result['page']}"
                    )
                    seen_sources.add(source_key)

        print()


        # -----------------------------------
        # Automatic Memory Extraction
        # -----------------------------------

        extraction_prompt = f"""
Analyze the user's message below.

Identify whether it contains information about the user
that could be useful in future conversations.

Examples:
- long-term goals
- education
- career goals
- skills
- projects
- learning goals
- important plans

Do NOT save:
- casual conversation
- temporary situations
- greetings
- questions
- information about other people

If there is useful long-term information, return ONLY
one short sentence.

If there is nothing important to remember, return exactly:

NONE

User message:
{user_input}
"""

        memory_chat = client.chats.create(
            model="gemini-3.5-flash"
        )

        memory_response = memory_chat.send_message(
            message=extraction_prompt
        )

        new_memory = memory_response.text.strip()

        if new_memory and new_memory.upper() != "NONE":
            save_memory(new_memory)
            print("⭐ Memory saved:", new_memory)
            print()


    except KeyboardInterrupt:
        print("\nLazizbek AI: Goodbye! 👋")
        break

    except Exception as e:
        print()
        print("❌ ERROR:", repr(e))
        print()
