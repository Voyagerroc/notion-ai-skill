# Copies skill files only; no shell profiles, aliases, credentials or network calls.
param(
    [string]$HomeDirectory = "",
    [string]$PythonExecutable = "python",
    [switch]$DryRun
)
$ErrorActionPreference = "Stop"
$InstallerArgs = @((Join-Path $PSScriptRoot "scripts/install_skill.py"))
if ($HomeDirectory) { $InstallerArgs += @("--home", $HomeDirectory) }
if ($DryRun) { $InstallerArgs += "--dry-run" }
& $PythonExecutable @InstallerArgs
exit $LASTEXITCODE
