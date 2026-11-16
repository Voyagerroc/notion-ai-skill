"""Copy documented skill files; never install aliases or inspect account state."""

import argparse
from pathlib import Path
import shutil

VERSION = "0.1.0"
SOURCE = Path(__file__).resolve().parents[1]
TARGETS = {
    "agents": Path(".agents/skills/notion-ai"),
    "claude": Path(".claude/skills/notion-ai"),
    "codex": Path(".codex/skills/notion-ai"),
}
FILES = ["SKILL.md", "AGENTS.md", "CLAUDE.md", "CODEX.md", "KIMI.md", "scripts/hybrid_runner.py"]


def install(home: Path, targets: list[str], dry_run: bool = False) -> list[Path]:
    home = home.expanduser().resolve()
    destinations = [home / TARGETS[name] / filename for name in targets for filename in FILES]
    # Validate the complete operation before the first directory or file is written.
    for filename in FILES:
        if not (SOURCE / filename).is_file():
            raise ValueError(f"Incomplete checkout: missing {filename}")
    for destination in destinations:
        if not destination.resolve().is_relative_to(home):
            raise ValueError("An existing symlink redirects the installation outside the selected home")
    if not dry_run:
        for name in targets:
            for filename in FILES:
                destination = home / TARGETS[name] / filename
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(SOURCE / filename, destination)
    return destinations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Target home (default: current user)")
    parser.add_argument("--target", action="append", choices=sorted(TARGETS), help="Repeat to select clients")
    parser.add_argument("--dry-run", action="store_true", help="Show destinations without writing")
    args = parser.parse_args()
    try:
        destinations = install(args.home, args.target or list(TARGETS), args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Installation failed: {exc}\n")
    for path in destinations:
        print(f"{'Would copy' if args.dry_run else 'Copied'}: {path}")
    executable = shutil.which("voyager-relay") or shutil.which("notion-ai")
    if executable:
        print("Bridge executable found on PATH. Authentication/model access was not checked.")
    else:
        print("Bridge CLI not found. Install notion2api 0.1.0+ and activate its environment first.")
    print("Only the selected skill directories were configured. Other clients need their guide/manual setup.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
