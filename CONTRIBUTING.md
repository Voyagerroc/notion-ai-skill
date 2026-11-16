# Contributing

Use Python 3.10+; the installer, runner and tests use only the standard library.

```console
python -m unittest discover -s tests -v
python scripts/install_skill.py --dry-run --home ./temporary-home
python scripts/hybrid_runner.py --help
```

Tests create temporary homes and an executable stub bridge. They must not invoke the real Notion bridge, read operator credentials or contact providers. Windows CI exercises the actual PowerShell wrapper; Linux CI exercises Bash. Test content packaging, process errors, cleanup and installed files rather than claiming model quality from mock outputs.

Keep changes focused and document actual supported client paths. Client guides are recipes, not proof of compatibility with every client release. The installer must not create aliases, alter PATH/profiles or inspect sessions. Review outgoing context and do not include tokens, private prompts, workspace IDs or user data in fixtures/issues. See [SECURITY.md](SECURITY.md).

Use the existing MIT license. PR descriptions should name actual validation and remaining limits; no guaranteed review time is offered.
