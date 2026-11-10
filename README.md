# VoyagerRelay

**Give your local agent hands. Give it a reasoning brain.**

VoyagerRelay is an open-source hybrid orchestration skill by **Voyagerroc Technologies**. It connects local coding agents to Notion AI through the [`notion2api`](https://github.com/Voyagerroc/notion2api) bridge: the local agent gathers context and executes work; Notion AI helps reason about the task and generate code.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Multi-Agent Spec](https://img.shields.io/badge/Spec-Multi--Agent-purple)](AGENTS.md)
[![Zero-Cost LLM](https://img.shields.io/badge/LLM-No%20Separate%20API%20Key-green)](#cost-and-availability)

> [!NOTE]
> This repository is currently named [`notion-ai-skill`](https://github.com/Voyagerroc/notion-ai-skill). **VoyagerRelay** is the orchestration workflow described here; `notion-ai` is the CLI provided by the separate `notion2api` project.

## Why VoyagerRelay?

Powerful coding workflows often face two constraints:

- **Metered inference can add up.** Large prompts, repeated refactoring, and multi-file analysis can consume substantial API tokens.
- **Cloud reasoning needs local context.** A cloud model does not automatically see your repository or run commands on your machine. A local agent must collect the relevant context and perform local actions.

VoyagerRelay joins the two:

1. A **local agent** reads selected files and prepares the task.
2. The **Notion AI bridge** sends the prompt to an available model.
3. The local agent reviews the response, applies changes, and runs tests.

The repository provides agent instructions, installers, and a Python prompt-packaging runner. The CLI and model connection are supplied by `notion2api`.

### Cost and availability

**“Zero-cost LLM” means no separate metered model-provider API key is required for the intended bridge workflow—not that inference or the overall workflow is guaranteed to be free.** Notion plans, credits, quotas, model availability, and local-agent charges can still apply. Check your account’s current terms and usage before relying on this workflow.

The bridge uses Notion’s web interface through an unofficial integration. Authentication or service behavior can change, and use is subject to applicable service terms.

### 💡 Credit Pools & Auto-Fallback Protection

Notion AI operates a dual-pool credit system:
* **Standard Credits (Auto Mode):** 1,500+ credits/month per member (with workspace credit overflow pooling). When set to `auto`, Notion dynamically routes tasks using lightweight models for simple questions and heavy models for complex code, drawing strictly from Standard Credits.
* **Select Credits (Manual Selection):** Typically capped at 500 credits/month per member (with rolling 6-hour throttles). Explicitly forcing high-end models like Claude Opus or Sonnet consumes this restricted pool. Once exhausted, the Notion web interface grays out model selection and restricts users to Auto mode.

**VoyagerRelay's Built-in Protection:**
1. **Default to `auto`:** Prompts sent without `-m` default to `auto`, preserving your precious Select Credits.
2. **Zero-Downtime Auto-Fallback:** If you specify `-m opus` or `-m sonnet` and hit a model rate limit (HTTP 429), quota restriction, or model unavailability, VoyagerRelay automatically catches the error, displays an informative recovery notice, and seamlessly re-routes the task to `auto` mode without interrupting your workflow.

## Architecture

```text
                         Your task
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ LOCAL AGENT — hands and carrier                          │
│ Antigravity · Claude Code · Codex · Cursor · Kimi       │
│                                                          │
│ Read selected files • Package context • Run commands     │
│ Review and apply changes • Execute tests                 │
└────────────────────────────┬─────────────────────────────┘
                             │
                    Prompt + selected context
                    notion-ai / prompt file (-P)
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ NOTION AI — reasoning and code-generation brain         │
│ Sonnet · Opus · GPT · Kimi, where available              │
│                                                          │
│ Analyze • Design • Generate • Explain                    │
└────────────────────────────┬─────────────────────────────┘
                             │
                       Response / code
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ LOCAL AGENT — review and verification                   │
│ Inspect diff • Apply changes • Run tests • Iterate      │
└──────────────────────────────────────────────────────────┘
```

This is a **workflow**, not a guarantee of autonomous execution: the capabilities available depend on the agent, its permissions, the bridge, and your configuration. Review generated code and test results before committing or deploying.

## Supported agents

| Agent | Intended integration | Guide |
|---|---|---|
| **Google Antigravity** | Installed skill and local hybrid runner | [SKILL.md](SKILL.md) |
| **Anthropic Claude Code** | Installed skill and agent instructions | [CLAUDE.md](CLAUDE.md) |
| **OpenAI Codex / Cursor** | CLI invocation; compatible clients can use the local OpenAI-compatible endpoint | [CODEX.md](CODEX.md) |
| **Moonshot Kimi** | Agent workflow and the `-m kimi` model alias | [KIMI.md](KIMI.md) |
| **Other local agents** | Follow the shared instructions and invoke the CLI | [AGENTS.md](AGENTS.md) |

## 🔐 Authentication & Account Management

VoyagerRelay supports multi-account management and dedicated authentication commands directly from the CLI.

### Connect Your Notion Account

Each user connects their own Notion account. You do not need a paid third-party API key—your Notion AI subscription covers inference:

```bash
# Automated Browser Login (Launches local Chrome/Edge, logs in, captures session via CDP)
voyager-relay login

# Manual Login (Masked input: safely paste token_v2 without exposing it on screen)
voyager-relay login --manual
```

> [!TIP]
> Both `voyager-relay` and `notion-ai` CLI aliases support the same subcommands interchangeably.

### Check Current Session and Workspace

Verify which Notion profile and workspace are active before sending prompts:

```bash
voyager-relay whoami
# or
voyager-relay status
```

Output preview:
```text
[VoyagerRelay Auth Durumu]
✓ Aktif Profil : default
  Kullanıcı     : Erol Taşcı (tascierol24@gmail.com)
  Workspace ID  : a8f418f1-c7bd-4411-9127-0bde7d7c8667
  Toplam Profil : 1
  Durum         : Bağlı ve aktif (Tüm sorgular $0 maliyetle akar)
```

### Log Out and Clear Local Credentials

To safely remove saved tokens, session history, and environment entries from your local machine:

```bash
voyager-relay logout
```

> [!NOTE]
> `voyager-relay logout` clears credentials from your local machine (`accounts.json`, `.env`, and session cache). To invalidate the session on Notion's servers, sign out through Notion's web settings.

### Agent Privacy & Security Mandates

- **Zero Third-Party Relays:** All prompts, file contexts, and tokens communicate directly with Notion's web infrastructure over HTTPS.
- **Agent Chat Isolation:** AI coding agents (Antigravity, Claude Code, Codex, Kimi) are strictly instructed to **NEVER** ask users to paste `token_v2`, passwords, or session cookies into chat conversations.
- **Masked Terminal Input:** During manual login (`--manual`), inputs are masked using `getpass` to prevent credentials from being exposed in screenshots, terminal history, or recordings.

---

## ⚡ 1-Minute Quickstart

The skill installation takes about a minute **once the prerequisites are ready**.

### Prerequisites

- Git and Python 3.10+
- An eligible Notion account with AI access
- A configured [`notion2api`](https://github.com/Voyagerroc/notion2api) installation
- A local agent you want to use

Set up the bridge first:

```bash
git clone https://github.com/Voyagerroc/notion2api.git
cd notion2api
python -m pip install -r requirements.txt
python login.py
```

Follow the bridge’s setup instructions to make `notion-ai` available on your `PATH`. You can also run `python ask_notion.py` directly from the `notion2api` directory; substitute it for `notion-ai` in the examples below. Return to the directory where you want to clone VoyagerRelay.

### Install the skill

**Linux / macOS:**

```bash
git clone https://github.com/Voyagerroc/notion-ai-skill.git && cd notion-ai-skill && chmod +x install.sh && ./install.sh
```

**Windows PowerShell:**

```powershell
git clone https://github.com/Voyagerroc/notion-ai-skill.git; Set-Location notion-ai-skill; .\install.ps1
```

Verify the bridge:

```bash
notion-ai --list-models
notion-ai -m sonnet "Explain this project in three sentences."
```

## CLI usage

The following examples use the `notion-ai` CLI from `notion2api`. Run them from your project directory unless noted otherwise.

### Ask a question

```bash
notion-ai "Explain the trade-offs of an event-driven architecture."
```

### Choose a model

```bash
notion-ai -m sonnet "Review this design for maintainability."
notion-ai -m opus "Analyze failure modes in a distributed job queue."
notion-ai -m kimi "Identify concurrency risks in this pipeline."
notion-ai -m gpt "Design a bounded worker pool."
```

### Include local files with `-f`

```bash
notion-ai -m sonnet \
  -f src/server.py \
  -f src/config.py \
  "Explain the request flow and identify configuration risks."
```

### Read a prompt from a file with `-P`

For larger instructions, write the prompt to a UTF-8 text file:

```bash
notion-ai -m opus -P prompt.txt -f src/service.py
```

`-P` avoids putting the full prompt on the command line, bypassing OS argument length limits.

### Edit a file with `-e`

```bash
notion-ai -m sonnet -e src/service.py "Add input validation and explicit error handling."
```

To restore the backup:

```bash
notion-ai --rollback src/service.py
```

### Start the interactive REPL

```bash
notion-ai
```

Inside the session:

```text
/model sonnet
/model opus
new
exit
```

### Hybrid runner

```bash
python scripts/hybrid_runner.py \
  "Review this service for error-handling gaps." \
  -m sonnet \
  -f src/service.py src/config.py
```

## Local OpenAI-compatible endpoint

`notion2api` also documents a local server for compatible clients. From the `notion2api` directory:

```bash
python -m uvicorn app.server:app --host 127.0.0.1 --port 8765
```

Configure a compatible client with:

```text
Base URL: http://127.0.0.1:8765/v1
Chat endpoint: http://127.0.0.1:8765/v1/chat/completions
```

## Security and responsible use

- **Protect credentials.** Treat Notion session data and bridge configuration as secrets. Never commit them to Git.
- **Review outgoing context.** Prompts and files passed to the bridge leave your local machine.
- **Inspect generated changes.** AI-generated code can be incorrect, insecure, or incomplete.
- **Run your own checks.** Execute relevant tests, linters, and security checks before merging.
- **Use least privilege.** Grant local agents only the filesystem and command access needed for the task.

## Troubleshooting

| Problem | What to check |
|---|---|
| `notion-ai` is not found | Configure the bridge executable on `PATH`, or run `python ask_notion.py` from the `notion2api` directory. |
| Authentication fails | Revisit `notion2api` setup and login; verify the account has AI access. |
| A model alias fails | Check `notion-ai --list-models` and your account’s available models. |
| The installer cannot find files | Run it from a complete repository checkout; the script expects adjacent repository files. |
| A file is missing from context | Check the path relative to your current directory and confirm you have permission to read it. |
| A patch or rollback fails | Inspect the CLI output, verify the target and backup, and use version control to recover if needed. |
| A client cannot connect | Confirm the bridge server is running on `127.0.0.1:8765` and the client uses the `/v1` base URL. |

## Contributing

Contributions are welcome—from documentation and agent integrations to bug reports and workflow improvements.

For agent-specific conventions, see [AGENTS.md](AGENTS.md). Never include credentials, session tokens, or private project data in an issue or pull request.

## License

VoyagerRelay is distributed under the [MIT License](LICENSE).

Built by **Voyagerroc Technologies** and the open-source community.
