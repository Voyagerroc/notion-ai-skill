# Security policy

Fixes target latest `main` and the current preview. This experimental skill is an unofficial integration recipe, not a model service, encrypted vault, sandbox or compliance certification.

Report privately through [GitHub private reporting](https://github.com/Voyagerroc/notion-ai-skill/security/advisories/new), or **erol@voyagerroctechnologies.com** if unavailable. Give a synthetic reproduction and impact; do not include session tokens, passwords, private prompts or real account IDs. No bounty, response deadline or production support is promised.

The installer copies named files to selected skill directories. It neither installs the bridge nor changes aliases, PATH or shell profiles. The runner reads only explicitly selected context, caps it at 4 MiB, writes a temporary prompt, invokes the bridge without a shell and removes the prompt after success, failure or timeout. Forced process termination can leave a temporary file; review local temporary storage accordingly.

Prompts, file contents and selected file paths are sent through the separately configured bridge to its upstream. Review them before invocation. Never submit credentials or personal data without appropriate authorization. The provider host, credential storage, account access, cost and rate limits belong to the bridge/service configuration; this repository cannot certify them. Returned code requires human review and local tests before execution.
