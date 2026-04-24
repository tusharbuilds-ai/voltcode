# ⚡ VoltCode

> An open-source terminal AI coding agent inspired by Claude Code.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green)
![LangSmith](https://img.shields.io/badge/LangSmith-Monitored-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## What is VoltCode?

VoltCode is a terminal-based AI coding agent that classifies your intent, plans autonomously, and generates complete projects directly on your local filesystem — all from a single natural language description.

```
> What will you build today?
Build me a React todo app with authentication

[ 🧠 Planning... ]
✓ Intent: create
✓ Plan created: 8 steps
✓ Clarification: What styling framework?

> Tailwind CSS

[ ⚡ Building... ]
[1/8] Creating folder structure...
[2/8] Creating package.json...
[3/8] Creating src/App.jsx...
[4/8] Creating src/components/TodoList.jsx...
[5/8] Creating src/styles/globals.css...
...
✓ Project created in your working directory
```

---

## Features

- **Intent Classification** — Automatically detects if you want to create, edit, or ask a general question
- **Autonomous Planning** — Creates a step-by-step plan before executing complex projects
- **Clarification System** — Asks smart questions before writing code, not after
- **Local Filesystem Access** — Reads and writes files directly on your machine
- **Cross-Session Memory** — Remembers your conversations via Firebase Realtime Database
- **Sub-Agent Memory Management** — Dedicated summarization sub-agent keeps main context window clean
- **Production Observability** — Full LangSmith tracing on every run
- **Production Logging** — Structured logging with Loguru across all nodes

---

## Architecture

```
User Input
    ↓
think_node (Gemini 2.5 Flash)
→ Classifies intent
→ Creates execution plan
→ Reads rolling summary from Firebase
    ↓
route_after_thinking
    ↓
┌──────────────┬──────────────┬──────────────┐
clarify_node   write_node     general_node
(ask user)     (generate)     (answer Q&A)
                    ↓
               make_file_node
               (save to disk)
                    ↓
          summarization_subagent
          (isolated context — updates Firebase)
```

### Memory Architecture

VoltCode uses a **Sub-Agent Delegation Pattern** for context management:

- **Main Agent** receives: summary (≤500 chars) + last K messages + current query
- **Summarization Sub-Agent** runs in complete isolation, compresses old messages, returns clean paragraph
- **Firebase** stores summary + recent messages per session
- **limitToLast(k)** queries prevent fetching full history on every turn

This pattern reduced think_node latency from **16 seconds → 6 seconds** (measured via LangSmith).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | LangGraph |
| LLM (Planning) | Gemini 2.5 Flash |
| LLM (Summary) | Gemini 2.5 Flash Lite |
| LLM (Execution) | Gemini 3 Flash Preview |
| Memory | Firebase Realtime Database |
| Observability | LangSmith |
| Logging | Loguru |
| Output Control | Strict JSON parsing |

---

## Performance (via LangSmith)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| think_node latency | 16.52s | 6.06s | 63% faster |
| Summary model time | 6.27s | 1.75s | 72% faster |
| Tokens per query | 6.5K | ~3K | 54% reduction |
| Cost per query | $0.0113 | ~$0.003 | 73% cheaper |

---

## Installation

```bash
# Clone the repo
git clone https://github.com/tusharbuilds-ai/voltcode.git
cd voltcode

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Fill in your API keys
```

---

## Environment Variables

```env
GOOGLE_API_KEY=your_gemini_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=voltcode
FIREBASE_DATABASE_URL=your_firebase_url
```

---

## Usage

```bash
python app.py
```

```
⚡ VOLTCODE

> Volt Code need a working directory path to code. Give the path
C:\Users\yourname\projects

> What will you build today?
```

### Example Queries

```
# Create projects
"Build me a landing page for a fitness app"
"Create a Python calculator with GUI"
"Make a React dashboard with charts"

# Ask questions
"What design patterns should I use for this?"
"Explain the difference between REST and GraphQL"

# Edit (coming soon)
"Add dark mode to the existing project"
"Fix the authentication bug"
```

---

## Project Structure

```
voltcode/
├── config/          ← Model config, temperature, working directory
├── graph/           ← LangGraph nodes and conditional routes
├── helper/          ← Utility functions
├── LLM/             ← LLM initialization
├── logs/            ← Loguru log files
├── memory/          ← Firebase memory management
├── nodes/           ← Individual agent nodes
├── prompt/          ← All system prompts
├── subagents/       ← Summarization sub-agent
├── voltcode/        ← Core application
├── app.py           ← Entry point
└── requirements.txt
```

---

## Roadmap

- [x] Intent classification (create/edit/general)
- [x] File and folder generation
- [x] Cross-session Firebase memory
- [x] Sub-agent context management
- [x] LangSmith observability
- [x] Loguru production logging
- [ ] Edit existing files
- [ ] Complex project planning with progress tracking
- [ ] PyPI package (`pip install voltcode`)
- [ ] Web terminal interface

---

## Certifications

Built using knowledge from:
- **Anthropic — Introduction to Sub-Agents** (Applied for memory architecture)
- **Anthropic — Introduction to Model Context Protocol**

---

## Author

**Tushar Jain** — Agentic AI Engineer  
[GitHub](https://github.com/tusharbuilds-ai) · [LinkedIn](https://linkedin.com/in/tusharjain2003)

---

## License

MIT License — feel free to use, modify, and distribute.
