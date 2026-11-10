# CODEX.md - OpenAI Codex & Cursor Integration Guide

This guide defines how **OpenAI Codex**, **Cursor**, **Windsurf**, and **Aider** agents leverage the `notion-ai` local bridge.

---

## 🔐 Authentication & Security

Before launching the server or invoking models:
1. Verify credentials: `voyager-relay whoami`
2. If unauthenticated, instruct user: `voyager-relay login`
3. Never prompt for or ingest `token_v2` in model completions or conversation context.

---

## 🚀 Two Integration Modes

### Mode 1: Local OpenAI-Compatible Server (Recommended for Cursor & Aider)
The Notion AI bridge includes a high-performance FastAPI server exposing standard OpenAI `/v1/chat/completions` endpoints.

1. **Start the local server:**
   ```bash
   notion-ai-server
   # Or directly:
   python -m uvicorn app.server:app --port 8765
   ```
2. **Configure Codex / Cursor / Aider:**
   * **OpenAI Base URL:** `http://127.0.0.1:8765/v1`
   * **API Key:** Any arbitrary string (e.g. `notion`) or your configured `API_KEY`.
   * **Available Models:**
     * `claude-sonnet4.6`
     * `claude-opus4.6`
     * `gpt-5.5`
     * `kimi-2.7`
     * `deepseek-v4pro`
     * `gemini-3.5flash`
     * `auto`

### Mode 2: Shell Tool Execution (Codex CLI / Agent Harness)
Codex agents can invoke the CLI wrapper directly:

```bash
# Ask GPT-5.5 via Notion AI
notion-ai -m gpt "Write a concurrent worker pool in Go"

# Ask Claude Sonnet via Notion AI
notion-ai -m sonnet "Optimize SQL queries in repository"

# Feed files directly
notion-ai -m gpt -f schema.prisma "Generate seed data script"
```

---

## ⚡ Benefits for Codex Users
* Eliminates OpenAI token billings for heavy background drafting.
* Grants instant access to Claude 3.5 Sonnet and Opus directly inside OpenAI-centric tooling.
