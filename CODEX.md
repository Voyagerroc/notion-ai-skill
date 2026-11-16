# Codex / compatible-client recipe

Install notion2api 0.1.0+ and activate its environment. `notion-ai`, `voyager-relay` and `notion-ai-server` are installed console commands; no external wrapper aliases are required.

Use `notion-ai -P prompt.txt` only for authorized provider work. Review selected context first and keep credentials out of chat, prompt files and logs. Generated patches require review and actual tests.

For clients supporting a custom OpenAI-compatible endpoint, start `notion-ai-server --host 127.0.0.1 --port 8765`; configure base URL `http://127.0.0.1:8765/v1` and the bridge's configured API key. Do not assume every client supports this mode or disable authentication to make it connect. Client integration and live model access require separate validation.

Authentication is a local user action through `voyager-relay login`; `--help` is account-free. No model, cost or fallback guarantee is made. See SKILL.md and SECURITY.md.
