# Kimi recipe

The bridge contains a local `kimi` alias. Actual account access and model availability are provider-dependent; no specific model generation, quota, latency or free-use promise is made.

After installing the notion2api bridge and activating its environment, an authorized task can use `notion-ai -m kimi -P prompt.txt`. Check local mappings with `notion-ai --list-models`; that list does not contact the provider.

The installer supplies this guide but does not configure a Kimi client automatically. Set up and validate the chosen client's shell/endpoint integration manually. Keep credentials local, review outgoing context and test returned code. See SKILL.md and SECURITY.md.
