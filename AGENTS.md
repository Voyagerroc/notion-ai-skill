# AGENTS.md - Universal AI Agent Instructions

This document specifies the integration protocol for autonomous AI coding agents (Antigravity, Claude Code, Codex, Kimi, Cursor, Aider, Devin-like harnesses) interacting with this environment.

---

## 🧭 Multi-Agent Role Division

```
┌────────────────────────────────────────────────────────┐
│                   LOCAL AI AGENT                       │
│  (Antigravity / Claude Code / Codex / Kimi / Cursor)   │
│                                                        │
│  • Reads project repository and local configuration    │
│  • Manages memory (NotebookLM, Graphify, SQLite)       │
│  • Executes shell commands, linters, and unit tests   │
│  • Performs atomic file writes and commits             │
└──────────────────────────┬─────────────────────────────┘
                           │
             Delegates heavy generation ($0)
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
└────────────────────────────────────────────────────────┘
```

---

## 📋 Agent Rules of Engagement

1. **Token Cost Routing:** Whenever generating long code files, comprehensive documentation, or extensive refactoring, execute `notion-ai -m sonnet -P <prompt_file>` instead of calling paid cloud API credits.
2. **Context Passing:** Always pass file dependencies using `-f <file>` or package them into a temporary file with `-P <file>` to avoid shell argument truncations.
3. **AST Validation:** Verify that code modifications compile and pass project unit tests before declaring task completion.
4. **Rollback Safety:** If a patch introduces regressions, run `notion-ai --rollback <target_file>`.
5. **Authentication & Privacy Protection:**
   - Run `voyager-relay whoami` to check connection state.
   - If not logged in, prompt user to run `voyager-relay login` (or `voyager-relay login --manual`).
   - **CRITICAL:** Never ask user to paste raw tokens, passwords, or session cookies into the conversation. Tokens must stay in the local secure environment.
