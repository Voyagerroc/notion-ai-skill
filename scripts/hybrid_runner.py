#!/usr/bin/env python3
"""Package explicitly selected context and call the separately installed bridge."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

MAX_CONTEXT_BYTES = 4 * 1024 * 1024


def find_bridge() -> list[str]:
    for name in ("voyager-relay", "notion-ai"):
        executable = shutil.which(name)
        if executable and not (os.name == "nt" and Path(executable).suffix.lower() in (".cmd", ".bat")):
            return [executable]
    raise RuntimeError("Bridge CLI missing. Install notion2api 0.1.0+ and activate its environment; use its console executables.")


def package_prompt(task: str, files: list[str] | None = None) -> str:
    parts = [task]
    remaining = MAX_CONTEXT_BYTES - len(task.encode("utf-8"))
    for filename in files or []:
        path = Path(filename).expanduser().resolve(strict=True)
        if not path.is_file():
            raise ValueError(f"Context must be a regular file: {filename}")
        with path.open("rb") as stream:
            content = stream.read(max(0, remaining) + 1)
        if len(content) > remaining:
            raise ValueError("Selected context exceeds the 4 MiB limit")
        section = f"\n\n--- FILE: {path} ---\n```\n{content.decode('utf-8', errors='replace')}\n```"
        remaining -= len(section.encode("utf-8"))
        parts.append(section)
    if remaining < 0:
        raise ValueError("Selected context exceeds the 4 MiB limit")
    return "".join(parts)


def run_hybrid_task(task: str, files: list[str] | None = None, model: str = "auto",
                    think: bool = False, *, bridge_command: list[str] | None = None,
                    timeout: float = 300) -> str:
    command = list(bridge_command) if bridge_command is not None else find_bridge()
    prompt = package_prompt(task, files)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as stream:
        stream.write(prompt)
        prompt_path = stream.name
    try:
        command += ["-m", model, "-P", prompt_path]
        if think:
            command.append("-t")
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=timeout, shell=False)
        if result.returncode:
            # Provider stderr can contain account data. Do not echo it through agent logs.
            raise RuntimeError(f"Bridge exited with code {result.returncode}; inspect it locally without sharing credentials")
        return result.stdout.strip()
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Bridge timed out; no availability or automatic recovery is guaranteed") from exc
    finally:
        Path(prompt_path).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", help="Instruction for the bridge (sent to the configured provider)")
    parser.add_argument("-f", "--files", nargs="*", help="Only these selected files are read")
    parser.add_argument("-m", "--model", default="auto", help="Bridge model alias; availability is account-dependent")
    parser.add_argument("-t", "--think", action="store_true")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    try:
        output = run_hybrid_task(args.task, args.files, args.model, args.think)
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Runner failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
