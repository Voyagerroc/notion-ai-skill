# VoyagerRelay skill

An experimental prompt-packaging workflow for local coding agents, using the separate [notion2api bridge](https://github.com/Voyagerroc/notion2api). The local agent selects context, reviews responses and runs checks. This repository supplies skill files, a standard-library installer and a runner; it does not supply model access.

[![Offline skill checks](https://github.com/Voyagerroc/notion-ai-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Voyagerroc/notion-ai-skill/actions/workflows/ci.yml)
[![MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Illustrative flow below, **not captured model output or a test result**:

```text
Selected files + task -> temporary prompt -> installed bridge
                                           |
Local review + real tests <- response -----+
```

## Install the bridge first

Use Python 3.10+ and Git. The bridge's 0.1.0 preview provides real `notion-ai`, `voyager-relay` and `notion-ai-server` console commands.

```console
git clone https://github.com/Voyagerroc/notion2api.git
cd notion2api
python -m venv .venv
```

Activate `.venv` with `.venv\Scripts\Activate.ps1` in Windows PowerShell or `source .venv/bin/activate` on Linux/macOS, then:

```console
python -m pip install -e .
notion-ai --help
voyager-relay --help
notion-ai-server --help
```

Commands work from any directory while that environment is activated. For persistent user commands, the bridge also supports `uv tool install --editable .`; ensure the path reported by `uv tool dir --bin` is on PATH. Do not copy or rename command wrappers. `--help` requires no account and does not read credentials. See the bridge's README for state locations and locked development setup.

Only when ready to use the service, run `voyager-relay login` in your **local interactive terminal**, using your own eligible account. Never paste credentials into agent chat. `whoami` reports saved local configuration, not proof of a live session or zero cost.

## Install the skill

Return to your projects directory, clone this repository, then use the portable installer:

```console
git clone https://github.com/Voyagerroc/notion-ai-skill.git
cd notion-ai-skill
python scripts/install_skill.py --dry-run
python scripts/install_skill.py
```

Equivalent wrappers: `bash install.sh` on Linux/macOS, or `.\install.ps1` in Windows PowerShell. To use an explicit test home: `python scripts/install_skill.py --home ./temporary-home`. The PowerShell wrapper takes `-HomeDirectory <path>` and optional `-PythonExecutable <path>`.

The default installer copies `SKILL.md`, all four agent guides and `scripts/hybrid_runner.py` into these **actual** directories:

| Target | Directory |
| --- | --- |
| Shared agents / Antigravity | `~/.agents/skills/notion-ai` |
| Claude Code | `~/.claude/skills/notion-ai` |
| Codex legacy skill path | `~/.codex/skills/notion-ai` |

Use repeated `--target agents`, `--target claude` or `--target codex` to select clients. Other clients, including Kimi/Cursor, need their guide and manual client configuration; installing files is not verification of client compatibility. Existing named skill files are replaced; unrelated files are preserved. The installer does not install the bridge, register aliases, alter PATH/profiles, log in or inspect credentials.

## Runner

```console
python scripts/hybrid_runner.py "Review error handling" -f src/service.py -m auto
```

Strict context validation is the default: missing, unreadable or directory inputs fail before the bridge is invoked. The runner requires an installed bridge on PATH, reads only selected files, limits total UTF-8 context to 4 MiB and passes it in a temporary `-P` prompt file. It uses structured process arguments without a shell and removes the prompt after success, nonzero exit or timeout. On Windows use the bridge's pip-installed console executables; copied `.cmd`/`.bat` wrappers are unsupported. Abrupt process termination can leave temporary files.

`-o response.txt` saves the returned text; it does not apply or execute code. Review outgoing paths/content and returned changes yourself. The runner has no automatic retry or guarantee of fallback/availability. The configured bridge controls upstream behavior.

## Bridge recipes

```console
notion-ai -P prompt.txt
notion-ai -m auto -f src/service.py "Review this source"
notion-ai -e src/service.py "Propose clearer error handling"
notion-ai --rollback src/service.py
notion-ai-server --host 127.0.0.1 --port 8765
```

The optional local server uses `http://127.0.0.1:8765/v1` for compatible clients. Model names from `notion-ai --list-models` are local mappings, not an account-availability guarantee. Patching syntax checks are not an OS sandbox or proof of correctness. Direct workspace publishing additionally needs the separately configured `ntn` CLI. See [AGENTS.md](AGENTS.md), [CLAUDE.md](CLAUDE.md), [CODEX.md](CODEX.md) and [KIMI.md](KIMI.md).

<a id="cost-and-availability"></a>

## Cost, privacy and support boundary

This is an unofficial Notion web integration. Provider plans, quotas, models, authentication and terms can change. There is no guarantee of free inference, token savings, fixed credit allowances, latency or uninterrupted fallback. Local-agent charges can also apply.

Prompts, selected files and file paths leave your machine through the separately configured bridge. Review them before sending, keep credentials local and use synthetic fixtures in tests. No test in this repository contacts Notion or proves live model access. Read [SECURITY.md](SECURITY.md).

## Verification and contributions

```console
python -m unittest discover -s tests -v
python scripts/hybrid_runner.py --help
python scripts/install_skill.py --version
```

The offline suite runs a real executable stub bridge, temporary homes, failure/timeout cleanup and wrapper installations. CI exercises Windows PowerShell and Linux Bash separately. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for focused changes and privacy boundaries. Pick an existing issue or propose a concrete improvement; a response/merge time is not guaranteed.

Existing [MIT license](LICENSE). Preview version: **0.1.0**.
