# Windows task runner for Agents Blog.
# Usage: .\make.ps1 <target>
# Paired with Makefile. Native PowerShell only; this script does not call WSL.

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Target
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

function Get-NativeExitCode {
    if ($null -eq $global:LASTEXITCODE) {
        return 0
    }
    return $global:LASTEXITCODE
}

if ([string]::IsNullOrWhiteSpace($Target)) {
    [Console]::Error.WriteLine('Usage: .\make.ps1 <target>')
    exit 1
}

$Target = $Target.Trim()

$pending = @{
    setup      = 'setup: will install project dependencies once the stack is chosen'
    dev        = 'dev: will start the local development server once the stack is chosen'
    lint       = 'lint: no-op until the stack lands; will enforce zero lint warnings'
    format     = 'format: will format sources with Prettier and ruff once the stack is chosen'
    typecheck  = 'typecheck: no-op until the stack lands; will run the strict type checker'
    'test-e2e' = 'test-e2e: will run end-to-end tests once the stack is chosen'
    'test-bdd' = 'test-bdd: will run Gherkin journeys (subscribe, read post, search) once the stack is chosen'
    coverage   = 'coverage: no-op until the stack lands; core logic target is 100 percent and the CI gate is 80 percent'
    preview    = 'preview: will serve the production build once the stack is chosen'
    audit      = 'audit: will audit dependencies once the stack is chosen'
    release    = 'release: will cut a versioned release once the stack is chosen'
    clean      = 'clean: will remove local build artifacts once the stack is chosen'
}

if ($Target -eq 'test') {
    $testsDir = Join-Path $PSScriptRoot 'tests'
    if (Test-Path -LiteralPath $testsDir -PathType Container) {
        & python -m unittest discover -s tests -v
        exit (Get-NativeExitCode)
    }
    Write-Output 'test: no tests directory; nothing to run'
    exit 0
}

if ($Target -eq 'sync-agents') {
    $syncScript = Join-Path $PSScriptRoot 'scripts\sync-agents.ps1'
    if (Test-Path -LiteralPath $syncScript -PathType Leaf) {
        & powershell.exe -NoProfile -NonInteractive -File $syncScript
        exit (Get-NativeExitCode)
    }
    Write-Output 'sync-agents: scripts/sync-agents.ps1 not found; nothing to sync'
    exit 0
}

if ($Target -eq 'build') {
    Write-Output 'python -m compileall -q scripts tests'
    & python -m compileall -q scripts tests
    exit (Get-NativeExitCode)
}

if ($pending.ContainsKey($Target)) {
    Write-Output $pending[$Target]
    exit 0
}

[Console]::Error.WriteLine("Unknown target: $Target")
[Console]::Error.WriteLine('Usage: .\make.ps1 <target>')
exit 1
