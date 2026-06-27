# 🤖 AgentOS: The Operating System for AI Agents

> *A multi-agent system that lets AI agents discover, communicate, and collaborate autonomously — like an operating system, but for AI.*

---

## 🌟 What is AgentOS?

AgentOS is a Multi-Agent System built with Google ADK and Gemini AI that enables autonomous agent collaboration without hardcoded workflows.

**The Problem:**
Most multi-agent systems require developers to hardcode which agent talks to which. Adding a new agent means rewriting the entire pipeline.

**The Solution:**
AgentOS introduces an Agent Registry and Message Bus — agents register their capabilities and discover each other dynamically, just like apps on an operating system.

---

## 🎯 Modes

### 🌏 Mode 1: Research & Business Analysis
Orchestrates 3 agents to produce professional executive reports on any topic.

### 💻 Mode 2: Developer Assistant
Intelligently detects what you need and helps with code writing, bug fixing, explanation, code review, and test writing.

---

## 🏗️ Architecture

```
User Input
    ↓
[Orchestrator - main.py]
    ↓
[Agent Registry] ←→ [Message Bus]
    ↓
┌─────────────────────────────────────┐
│  Research    Analyst    Writer      │  ← Research Mode
│  Agent       Agent      Agent       │
├─────────────────────────────────────┤
│  Code Agent                         │  ← Developer Mode
│  (write/debug/explain/review/test)  │
└─────────────────────────────────────┘
    ↓
[Google Drive MCP] ← saves report automatically
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Google ADK 2.3.0 | Agent framework |
| Gemini 2.5 Flash | AI brain for all agents |
| MCP Google Drive | Save reports automatically |
| Python 3.14 | Core language |
| OAuth 2.0 | Security & authentication |

---

## ✅ Key Concepts Demonstrated

- ✅ **Multi-Agent System (ADK)** — Registry + Message Bus + Specialized Agents
- ✅ **MCP Server** — Google Drive integration saves reports automatically
- ✅ **Security** — .env for API keys, OAuth 2.0, .gitignore, audit trail
- ✅ **Agent Skills** — Code Agent with 5 specialized skills
- ✅ **Deployability** — Documented setup, virtual environment

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/chattip-gee/agentOS.git
cd agentOS
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install google-adk google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 5. Set up Google Drive MCP
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Enable Google Drive API
- Create OAuth 2.0 credentials
- Download as `credentials.json` and place in project root

### 6. Run AgentOS
```bash
python main.py
```

---

## 📁 Project Structure

```
agentOS/
├── main.py                 # Orchestrator & entry point
├── core/
│   ├── registry.py         # Agent Registry
│   └── message_bus.py      # Inter-agent communication
├── agents/
│   ├── research_agent.py   # Market research & analysis
│   ├── analyst_agent.py    # Strategic insights
│   ├── writer_agent.py     # Report writing
│   └── code_agent.py       # Developer assistant
├── tools/
│   └── drive_tool.py       # MCP Google Drive integration
├── .env.example            # Environment variables template
├── .gitignore              # Security - excludes secrets
└── README.md               # This file
```

---

## 🔐 Security

- API keys stored in `.env` — never committed to Git
- OAuth 2.0 for Google Drive authentication
- `token.json` excluded from version control
- Full audit trail via Message Bus

---

## 🌍 Vision

AgentOS is a proof of concept for **The Internet of Agents** — a future where AI agents from different providers (Gemini, Claude, GPT) can discover each other and collaborate through open protocols, just like devices on the internet.

---

*Built for Kaggle x Google AI Agents Intensive Capstone 2026*
*Track: Agents for Business*
