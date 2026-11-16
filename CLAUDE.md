# Claude Code recipe

Install the notion2api bridge and activate its environment first. If the user authorizes provider use, run `notion-ai -P prompt.txt` or the installed `scripts/hybrid_runner.py` with explicitly selected files. `notion-ai --help` is offline.

Review outgoing context and returned patches. Run real local tests after changes; do not treat a generated test claim as evidence. Use `-e` only for a user-authorized edit and review its diff; avoid automatic `-y` approval by default.

For account setup, direct the user to `voyager-relay login` in a local interactive terminal. Never ask for credentials in chat. Costs, quotas, models and service availability are account-dependent. See SKILL.md and SECURITY.md.
