# KIMI.md - Kimi (Moonshot AI) Integration Guide

Notion AI natively incorporates Moonshot AI's **Kimi** model family. This skill allows developers and agent harnesses to tap into Kimi without needing separate Moonshot API keys.

---

## 🔐 Authentication & Security

Ensure the Notion session is active before routing inference:
* Check status: `voyager-relay whoami`
* Sign in: `voyager-relay login` (or `voyager-relay login --manual`)
* Agent Rule: Never request raw session cookies or passwords in conversation.

---

## 🌟 Available Kimi Models

| Model Shortcut | Target Model Identifier | Description |
|---|---|---|
| `-m kimi` | `kimi-2.7` | Kimi K2.7 Code - High-context coding and reasoning model |
| `-m kimi-k3` | `kimi-k3` | Kimi K3 - Advanced multi-step mathematical & agentic reasoning |

---

## 💻 CLI Usage with Kimi

```bash
# 1. Quick coding task with Kimi K2.7
notion-ai -m kimi "Implement an LRU cache with TTL in TypeScript"

# 2. Analyze complex codebases using Kimi's deep context window
notion-ai -m kimi -f src/pipeline.ts -f src/worker.ts "Find bottlenecks and race conditions"

# 3. Large input via prompt file
notion-ai -m kimi -P large_context.txt

# 4. Safe code patching with Kimi
notion-ai -m kimi -e utils.py "Refactor functions to use generators"
```

---

## 🤖 Kimi CLI & Agent Workflows
Kimi-based autonomous agents can invoke `notion-ai` as their upstream inference router:
* **Cost:** $0 API fees (covered by Notion AI subscription).
* **Speed:** Low latency reverse-engineered TLS channel.
* **Output:** Clean stdout suitable for piping into shell pipelines or file patchers.
