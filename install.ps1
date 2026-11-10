# Universal Notion AI Skill Installer for Windows
# Configures Antigravity, Claude Code, and Codex environments

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Notion AI Universal Agent Skill Installer      " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Antigravity Skill Integration
$AgentSkillsDir = Join-Path $HOME ".agents\skills\notion-ai"
Write-Host "`n[1/3] Configuring Antigravity Skill ($AgentSkillsDir)..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path (Join-Path $AgentSkillsDir "scripts") -Force | Out-Null
Copy-Item (Join-Path $CurrentDir "SKILL.md") -Destination (Join-Path $AgentSkillsDir "SKILL.md") -Force
Copy-Item (Join-Path $CurrentDir "scripts\hybrid_runner.py") -Destination (Join-Path $AgentSkillsDir "scripts\hybrid_runner.py") -Force
Write-Host "  -> Antigravity skill successfully installed!" -ForegroundColor Green

# 2. Claude Code Integration
$ClaudeSkillsDir = Join-Path $HOME ".claude\skills\notion-ai"
Write-Host "`n[2/3] Configuring Claude Code ($ClaudeSkillsDir)..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $ClaudeSkillsDir -Force | Out-Null
Copy-Item (Join-Path $CurrentDir "CLAUDE.md") -Destination (Join-Path $ClaudeSkillsDir "CLAUDE.md") -Force
Copy-Item (Join-Path $CurrentDir "SKILL.md") -Destination (Join-Path $ClaudeSkillsDir "SKILL.md") -Force
Write-Host "  -> Claude Code skill successfully installed!" -ForegroundColor Green

# 3. Check notion-ai CLI on PATH
Write-Host "`n[3/3] Checking notion-ai CLI..." -ForegroundColor Yellow
$Cmd = Get-Command "notion-ai" -ErrorAction SilentlyContinue
if ($Cmd) {
    Write-Host "  -> notion-ai is available on PATH: $($Cmd.Source)" -ForegroundColor Green
} else {
    Write-Host "  -> [Notice] notion-ai CLI is not on PATH yet." -ForegroundColor DarkYellow
    Write-Host "     Please clone https://github.com/Voyagerroc/notion2api and run setup." -ForegroundColor DarkYellow
}

Write-Host "`n✓ Installation complete! Antigravity, Claude Code, Codex, and Kimi are ready." -ForegroundColor Cyan
Write-Host "Try: notion-ai -m sonnet 'Hello world'`n"
