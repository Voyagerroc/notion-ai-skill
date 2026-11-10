#!/usr/bin/env bash
# VoyagerRelay Universal Agent Skill Installer for Linux / macOS
# Configures Antigravity, Claude Code, and Codex environments

set -e

echo "=================================================="
echo "     VoyagerRelay — Universal Agent Skill         "
echo "=================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Antigravity Skill Integration
AGENT_SKILLS_DIR="$HOME/.agents/skills/notion-ai"
echo -e "\n[1/3] Configuring Antigravity Skill ($AGENT_SKILLS_DIR)..."
mkdir -p "$AGENT_SKILLS_DIR/scripts"
cp "$SCRIPT_DIR/SKILL.md" "$AGENT_SKILLS_DIR/SKILL.md"
cp "$SCRIPT_DIR/scripts/hybrid_runner.py" "$AGENT_SKILLS_DIR/scripts/hybrid_runner.py"
chmod +x "$AGENT_SKILLS_DIR/scripts/hybrid_runner.py"
echo "  -> Antigravity skill successfully installed!"

# 2. Claude Code Integration
CLAUDE_SKILLS_DIR="$HOME/.claude/skills/notion-ai"
echo -e "\n[2/3] Configuring Claude Code ($CLAUDE_SKILLS_DIR)..."
mkdir -p "$CLAUDE_SKILLS_DIR"
cp "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_SKILLS_DIR/CLAUDE.md"
cp "$SCRIPT_DIR/SKILL.md" "$CLAUDE_SKILLS_DIR/SKILL.md"
echo "  -> Claude Code skill successfully installed!"

# 3. Check notion-ai CLI
echo -e "\n[3/3] Checking notion-ai CLI..."
if command -v notion-ai >/dev/null 2>&1; then
    echo "  -> notion-ai is available: $(command -v notion-ai)"
else
    echo "  -> [Notice] notion-ai CLI not found in PATH."
    echo "     Please install https://github.com/Voyagerroc/notion2api first."
fi

echo -e "\n✓ Installation complete! Antigravity, Claude Code, Codex, and Kimi are ready.\n"
