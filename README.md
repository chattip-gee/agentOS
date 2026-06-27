# 🤖 AgentOS: The Operating System for AI Agents

> *A multi-provider AI agent system where Gemini, GLM, and DeepSeek collaborate autonomously to deliver better results than any single AI could alone.*

[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-2.3.0-orange)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash%20Lite-green)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🌟 What is AgentOS?

Most AI systems use a single LLM. AgentOS is different.

**AgentOS orchestrates multiple AI agents from different providers — Google, Zhipu AI, and DeepSeek — letting them collaborate like a team of specialists, each contributing their unique strengths.**

This is a proof of concept for **The Internet of Agents** — a future where AI agents from any provider can discover each other and collaborate through open protocols, just like devices on the internet.

---

## 💡 The Problem

Today's multi-agent systems are rigid:
- Agent A always calls Agent B — hardcoded, inflexible
- Adding a new agent requires rewriting the entire pipeline
- All agents use the same LLM — no diversity of intelligence
- No dynamic model selection based on task requirements

## 🚀 The Solution

AgentOS introduces:
- **Agent Registry** — agents register their capabilities dynamically
- **Message Bus** — agents communicate without direct coupling
- **Multi-Provider Orchestration** — different tasks go to the best LLM
- **Auto-Fallback** — if one provider fails, the system continues

---

## 🌍 Multi-Provider Architecture

```
🇺🇸 Gemini 2.5 Flash Lite  (Google)    — Research & Report Writing
🇨🇳 GLM-5.1               (Zhipu AI)  — Strategic Advisory
🇨🇳 DeepSeek-V4-Pro        (DeepSeek)  — Analysis, Validation & Code
```

**3 companies. 2 countries. 1 unified system.**

---

## 🏗️ Architecture

```
User Input
    ↓
[Orchestrator — main.py]
    ↓
[Agent Registry] ←→ [Message Bus]
    ↓
┌─────────────────────────────────────────────────┐
│           Specialized Agents                     │
│                                                  │
│  Research     Analyst    GLM      DeepSeek       │
│  Agent        Agent      Agent    Agent          │
│  (Gemini)     (DeepSeek) (GLM)    (DeepSeek)    │
│                                                  │
│  Writer       Code                               │
│  Agent        Agent                              │
│  (Gemini)     (DeepSeek)                         │
└─────────────────────────────────────────────────┘
    ↓
[MCP Google Drive] — Auto-saves report
    ↓
[Audit Trail] — Full message history
    ↓
Final Output
```

---

## 🎯 Two Modes

### 🌏 Mode 1: Research & Business Analysis
Multi-provider pipeline that produces professional executive reports.

```
Research Agent (Gemini)   → Gathers insights
Analyst Agent (DeepSeek)  → Strategic analysis  
GLM Agent (GLM-5.1)       → Strategic advisory
DeepSeek Agent            → Fact-checks & validates
Writer Agent (Gemini)     → Synthesizes final report
Google Drive (MCP)        → Auto-saves report
```

### 💻 Mode 2: Developer Assistant
AI-powered code help using DeepSeek — detects intent automatically.

```
write   → Writes production-ready code
debug   → Finds root cause and fixes bugs
explain → Explains concepts with examples
review  → Reviews code quality and suggests improvements
test    → Writes comprehensive test suites
```

---

## ✅ Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **Multi-Agent System (ADK)** | 6 specialized agents with Registry + Message Bus |
| **MCP Server** | Google Drive integration — auto-saves every report |
| **Security** | `.env` for secrets, OAuth 2.0, `.gitignore`, audit trail |
| **Agent Skills** | Code Agent with 5 auto-detected skills |
| **Multi-Provider** | Gemini + GLM + DeepSeek working together |
| **Deployability** | Virtual environment, documented setup, fallback handling |

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Google ADK | 2.3.0 | Agent framework |
| Gemini 2.5 Flash Lite | Latest | Research & writing |
| GLM-5.1 | Latest | Strategic advisory (Zhipu AI) |
| DeepSeek-V4-Pro | Latest | Analysis, validation & code |
| MCP Google Drive | v3 | Auto-save reports |
| Python | 3.14 | Core language |
| OAuth 2.0 | - | Google Drive authentication |

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
pip install google-adk anthropic google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_glm_api_key_here
ANTHROPIC_BASE_URL=https://your-gateway-url/
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 5. Set up Google Drive MCP
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a new project named `agentOS`
- Enable **Google Drive API**
- Create **OAuth 2.0 Client ID** (Desktop app)
- Download as `credentials.json` and place in project root
- Add your email as a test user in OAuth consent screen

### 6. Run AgentOS
```bash
python main.py
```

---

## 📁 Project Structure

```
agentOS/
├── main.py                  # Orchestrator & entry point
├── core/
│   ├── registry.py          # Agent Registry — dynamic discovery
│   └── message_bus.py       # Message Bus — inter-agent communication
├── agents/
│   ├── research_agent.py    # Gemini — market research & analysis
│   ├── analyst_agent.py     # DeepSeek — strategic analysis
│   ├── glm_agent.py         # GLM-5.1 — strategic advisory
│   ├── deepseek_agent.py    # DeepSeek — fact-checking & validation
│   ├── writer_agent.py      # Gemini — report synthesis
│   └── code_agent.py        # DeepSeek — developer assistant
├── tools/
│   └── drive_tool.py        # MCP Google Drive integration
├── credentials.json         # Google OAuth (gitignored)
├── .env                     # API keys (gitignored)
├── .env.example             # Environment variables template
├── .gitignore               # Security — excludes all secrets
└── README.md                # This file
```

---

## 🔐 Security

- API keys stored in `.env` — never committed to Git
- `credentials.json` and `token.json` excluded from version control
- OAuth 2.0 for Google Drive authentication
- Full audit trail via Message Bus for transparency
- Auto-fallback prevents single point of failure

---

## 🌍 The Vision: Internet of Agents

AgentOS demonstrates that AI agents from different providers can work together seamlessly. This is the foundation of a future where:

- Any AI agent can discover and collaborate with any other agent
- The best model is selected dynamically for each task
- No single company controls the entire AI stack
- Open protocols enable true cross-provider collaboration

Just like HTTP connected computers into the internet — AgentOS shows how open protocols can connect AI agents into **The Internet of Agents**.

---

## 📊 Example Output

Research Mode produces professional executive reports like:

```
# Executive Report: AI Agent Technology Trends in Japan 2025

## Executive Summary
Japan is at a critical juncture where AI Agent technology can transform 
its economy...

## Key Findings
• Accelerated enterprise adoption driven by labor shortages
• Government "Society 5.0" vision actively drives AI investment
• Strong focus on ethical AI frameworks

## Strategic Recommendations
1. Launch national AI agent talent programs
2. Develop legacy system integration frameworks  
3. Establish proactive regulatory frameworks

## Conclusion
Japan is uniquely positioned to lead in responsible AI agent deployment...

---
Generated by AgentOS | Powered by Gemini + GLM + DeepSeek
```

---

## 🏆 Built For

Kaggle x Google AI Agents Intensive Vibe Coding Capstone 2026
**Track: Agents for Business**

---

*AgentOS — Because the future of AI is collaboration, not competition.*
