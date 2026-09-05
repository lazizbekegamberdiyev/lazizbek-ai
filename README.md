````markdown
  🤖 Lazizbek AI

   Personal Data Science Copilot

Lazizbek AI is a modular personal AI copilot designed to support learning, programming, document analysis, research, and productivity.

The project goes beyond a traditional chatbot by combining **memory, RAG, web search, tool calling, AI agents, and intelligent request routing** into one system.

   🚀 Features

- 🧠  Conversation & Long-Term Memory — local SQLite storage
- 📚  Document RAG — semantic search across uploaded documents
- 🌐  Web Search — external and current information retrieval
- 🔧  Tool Calling** — calculator, Python execution, and file reading
- 🤖  AI Agent** — multi-step task execution
- 🚦  Intelligent Router** — selects the appropriate processing route
- 🖥️  Streamlit UI** — interactive chat interface

  🏗️ Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Intelligent Router
  │
  ├── Chat ──────► Gemini
  │
  ├── Web ───────► Web Search
  │
  ├── RAG ───────► ChromaDB
  │
  ├── Tool ──────► Calculator / Python / File
  │
  └── Agent ─────► Multi-step Tool Execution
                         │
                         ▼
                    Final Answer

              ┌──────────────┐
              │ SQLite       │
              │ Long-term    │
              │ Memory       │
              └──────────────┘
````

  🛠️ Tech Stack

"Programming"

* Python
* SQL

"AI & Data"

* Google Gemini API
* RAG
* Sentence Transformers
* ChromaDB
* SQLite

"Tools & Interface"

* Streamlit
* DDGS
* pypdf
* Git & GitHub

   📂 Project Structure

```text
lazizbek-ai/
│
├── app.py
├── main.py
├── memory.py
├── prompt.py
│
├── router.py
├── router_brain.py
├── router_executor.py
│
├── agent.py
├── agent_brain.py
├── agent_decision.py
├── agent_engine.py
├── agent_executor.py
├── agent_prompt.py
│
├── handlers/
│   ├── chat_handler.py
│   ├── web_handler.py
│   ├── rag_handler.py
│   ├── tool_handler.py
│   └── agent_handler.py
│
├── tools/
│   ├── calculator.py
│   ├── python_tool.py
│   ├── file_tool.py
│   ├── registry.py
│   └── executor.py
│
├── documents/
│
└── .gitignore
```

   🚦 Request Routing

The router classifies requests into five routes:

| Route    | Purpose                                           |
| -------- | ------------------------------------------------- |
| 💬 Chat  | General questions and learning                    |
| 🌐 Web   | Current or external information                   |
| 📚 RAG   | Questions about uploaded documents                |
| 🔧 Tool  | Simple tasks requiring one tool                   |
| 🤖 Agent | Multi-step tasks requiring planning and execution |

   🤖 Agent Workflow

For complex tasks, the agent can:

1. Understand the user's goal
2. Select an appropriate tool
3. Execute the tool
4. Inspect the result
5. Continue with another action when necessary
6. Produce a final answer

The current agent supports up to **5 execution steps**.

   🔐 Data & Security

The project is designed primarily for local development.

* API credentials are stored in `.env`
* `.env` is excluded from Git
* Conversation and long-term memory are stored locally in SQLite
* Uploaded documents remain in the local `documents/` directory
* RAG embeddings are stored locally in ChromaDB

> The Python tool uses restricted execution rules for this development project. It should not be considered a secure production sandbox.

   ⚙️ Installation

Clone the repository:

```bash
git clone git@github.com:lazizbekegamberdiyev/lazizbek-ai.git
cd lazizbek-ai
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install google-genai python-dotenv requests beautifulsoup4 ddgs pypdf chromadb sentence-transformers streamlit
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

   🎯 Project Goal

The main goal of Lazizbek AI is not simply to connect an LLM API.

It is a hands-on project for understanding how modern AI systems are built, including:

* Memory
* Retrieval
* Tool calling
* Planning
* Execution
* Agents
* Routing
* User interfaces

   📈 Development Roadmap

* [x] Gemini API
* [x] Conversation Memory
* [x] SQLite Permanent Memory
* [x] Personality / System Prompt
* [x] Automatic Long-Term Memory
* [x] Web Search
* [x] Document RAG
* [x] Tools
* [x] Multi-step Agent
* [x] Intelligent Router
* [x] Streamlit UI
* [ ] Deployment

   👨‍💻 About

Built by **Lazizbek Egamberdiyev**, an Economics & Data Science student at Westminster International University in Tashkent (WIUT).

The project is part of my journey toward building practical skills in **Python, Data Science, AI, and modern AI agent systems**.

---

⭐ Feel free to explore the code and follow the development.

```

**Hozir faqat paste qil. Commitni hali bosma.**
```
