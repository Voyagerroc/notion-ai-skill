# Universal Notion AI Agent Skill (`notion-ai-skill`)

> **Zero-Cost LLM Reasoning & Code Generation Bridge for Antigravity, Claude Code, Codex, and Kimi.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Universal Skill Spec](https://img.shields.io/badge/Skill%20Spec-Antigravity%20%7C%20Claude%20%7C%20Codex-blue.svg)](#)
[![Notion AI](https://img.shields.io/badge/Notion%20AI-Claude%20%7C%20GPT%20%7C%20Kimi-purple.svg)](#)

---

## 🌟 Overview / Genel Bakış

**`notion-ai-skill`** bridges modern autonomous coding agents (**Antigravity**, **Claude Code**, **OpenAI Codex**, and **Kimi**) with your **Notion AI subscription**, providing:

1. **$0 Marginal API Cost:** Route heavy multi-file reasoning, refactoring, and code generation through your Notion AI quota (including Notion for Startups) rather than paying metered per-token API fees.
2. **Local Agent Synergy:** Unlike Notion AI in a browser, your local agent acts as the **Eyes, Hands, and Memory** (file reading, AST parsing, compiler checks, git commits, and unit tests).
3. **Multi-Model Flexibility:** Switch between **Claude 3.5/Sonnet 4.6/Sonnet 5**, **Claude Opus**, **GPT-5.5**, **Kimi K2.7/K3**, **Gemini 3.5**, and **DeepSeek V4** with a single flag.
4. **Shell Length Bypass:** The `-P / --prompt-file` architecture safely handles large memory injections and context files without hitting OS terminal limits.

---

## 🤖 Supported Agent Environments

| Agent | Integration Mechanism | Documentation |
|---|---|---|
| **Google Antigravity (AGY)** | Native `SKILL.md` in `~/.agents/skills/notion-ai` | [SKILL.md](SKILL.md) |
| **Anthropic Claude Code** | Auto-injected `CLAUDE.md` + CLI / MCP tool | [CLAUDE.md](CLAUDE.md) |
| **OpenAI Codex / Cursor** | `CODEX.md` + Local OpenAI Endpoint (`:8765/v1`) | [CODEX.md](CODEX.md) |
| **Moonshot Kimi (K2.7/K3)**| Native Notion AI routing (`-m kimi`, `-m kimi-k3`) | [KIMI.md](KIMI.md) |
| **Universal / Aider / ECC**| Standard `AGENTS.md` and CLI runner | [AGENTS.md](AGENTS.md) |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│                   LOCAL AI AGENT                       │
│      (Antigravity / Claude Code / Codex / Kimi)        │
│                                                        │
│  • Reads project repository & local files              │
│  • Manages memory (NotebookLM, Graphify, SQLite)       │
│  • Executes tests, compilers, and linters              │
│  • Writes atomic code patches and creates commits      │
└──────────────────────────┬─────────────────────────────┘
                           │
             1. Gathers context & prepares prompt
             2. Injects via -P (file-based, no CLI limits)
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│               NOTION AI BRIDGE ENGINE                  │
│               (notion-ai / notion2api)                 │
│                                                        │
│  • Claude Sonnet 4.6 / 5.5                             │
│  • Claude Opus 4.6 / 5                                 │
│  • GPT-5.5 / GPT-6.1                                   │
│  • Kimi K2.7 / K3                                      │
│  • DeepSeek V4 Pro                                     │
│  • Zero-cost API token routing                         │
└──────────────────────────┬─────────────────────────────┘
                           │
             3. Clean response streamed back
                           ▼
┌────────────────────────────────────────────────────────┐
│             LOCAL EXECUTION & VERIFICATION             │
│  • Code applied to target files                        │
│  • Automated unit tests executed                       │
│  • AST knowledge graph & session log updated           │
└────────────────────────────────────────────────────────┘
```

---

## ⚡ 1-Minute Quick Start

### 1. Prerequisites
Ensure you have installed and authenticated [Voyagerroc/notion2api](https://github.com/Voyagerroc/notion2api):
```bash
git clone https://github.com/Voyagerroc/notion2api.git
cd notion2api
pip install -r requirements.txt
python login.py  # Captures Notion AI session
```

### 2. Install Skill

#### Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/Voyagerroc/notion-ai-skill/main/install.ps1 | iex
# Or locally:
.\install.ps1
```

#### Linux / macOS:
```bash
curl -fsSL https://raw.githubusercontent.com/Voyagerroc/notion-ai-skill/main/install.sh | bash
# Or locally:
chmod +x install.sh && ./install.sh
```

---

## 💻 Usage Examples

### 1. Simple Query
```bash
notion-ai "Explain async concurrency in Python with a code snippet"
```

### 2. Model Selection
```bash
# Claude Sonnet (default for coding)
notion-ai -m sonnet "Optimize this database query"

# Claude Opus (deep architecture)
notion-ai -m opus "Design an event-driven payment reconciliation system"

# GPT-5.5
notion-ai -m gpt "Write a concurrent worker pool in Go"

# Kimi K2.7 / K3 (Moonshot AI)
notion-ai -m kimi "Refactor this pipeline for maximum throughput"
```

### 3. File Context & Multi-File Feeding
```bash
notion-ai -m sonnet -f app/server.py -f app/config.py "Explain the middleware order"
```

### 4. Safe AST Code Patching with Rollback
```bash
# Preview diff and apply with syntax verification:
notion-ai -e app/tools.py "Add error handling and typing"

# Undo in 1 command if needed:
notion-ai --rollback app/tools.py
```

### 5. Interactive Chat REPL
Simply run without arguments in any terminal:
```bash
notion-ai
```
* Switch models on the fly: `/model sonnet` or `/model gpt`.
* Reset session: `new`.

---

## 🤝 Contributing

We welcome contributions, PRs, and agent integrations! Please see [AGENTS.md](AGENTS.md) for multi-agent guidelines.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

<p align="center">
  Crafted with ❤️ by <a href="https://github.com/Voyagerroc">Voyagerroc Technologies</a> and the AI agent community.
</p>
