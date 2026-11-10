#!/usr/bin/env python3
"""
Universal Hybrid Task Runner for AI Agents (Antigravity, Claude Code, Codex, Kimi).
Aggregates local files, builds safe unified prompts, passes them to notion-ai via -P,
and returns clean outputs without shell length limitations.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def run_hybrid_task(task: str, files: list = None, model: str = "sonnet", think: bool = False) -> str:
    files_context = ""
    if files:
        for fpath in files:
            fpath = os.path.abspath(fpath)
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    files_context += f"\n\n--- FILE: {fpath} ---\n```\n{content}\n```"
                except Exception as e:
                    print(f"[Warning] Failed to read file {fpath}: {e}", file=sys.stderr)
            else:
                print(f"[Warning] File not found: {fpath}", file=sys.stderr)

    full_prompt = task
    if files_context:
        full_prompt = f"{task}\n\nRelated Context Files:{files_context}"

    # Write to a temporary prompt file
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as tf:
        tf.write(full_prompt)
        prompt_path = tf.name

    executable = shutil.which("notion-ai") or "notion-ai"
    if sys.platform == "win32":
        cmd = ["cmd.exe", "/c", executable, "-m", model, "-P", prompt_path]
    else:
        cmd = [executable, "-m", model, "-P", prompt_path]

    if think:
        cmd.append("-t")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"notion-ai failed with code {result.returncode}: {err}")
        return result.stdout.strip()
    finally:
        try:
            os.remove(prompt_path)
        except OSError:
            pass


def main():
    parser = argparse.ArgumentParser(description="Universal Hybrid Agent Runner")
    parser.add_argument("task", help="Instruction or query for Notion AI")
    parser.add_argument("-f", "--files", nargs="*", help="Local files to feed into context")
    parser.add_argument("-m", "--model", default="sonnet", help="Model shortcut (sonnet, opus, gpt, gemini, kimi, deepseek)")
    parser.add_argument("-t", "--think", action="store_true", help="Display reasoning traces")
    parser.add_argument("-o", "--output", help="Optional path to save output file")

    args = parser.parse_args()
    output = run_hybrid_task(args.task, files=args.files, model=args.model, think=args.think)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[OK] Output saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
