# Copies .agents/skills into .claude/skills as real files.
# Safe to re-run. Does not create symlinks or junctions.
# .claude/agents/*.md is already the Claude agent location; write those
# files directly instead of linking them.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Remove-SkillDestination {
    <#
    .SYNOPSIS
        Removes a skill destination without following a link.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    $item = Get-Item -LiteralPath $Path -Force
    $reparse = [System.IO.FileAttributes]::ReparsePoint
    if (($item.Attributes -band $reparse) -eq $reparse) {
        # Delete the reparse point itself. Do not walk into its target.
        $item.Delete()
        return
    }
    Remove-Item -LiteralPath $Path -Recurse -Force
}

$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$SourceRoot = Join-Path $RepoRoot '.agents\skills'
$DestRoot = Join-Path $RepoRoot '.claude\skills'

if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) {
    Write-Error "Shared skills directory not found: $SourceRoot"
}

New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null

foreach ($skill in Get-ChildItem -LiteralPath $SourceRoot -Directory -Force) {
    $destination = Join-Path $DestRoot $skill.Name
    Remove-SkillDestination -Path $destination
    Copy-Item -LiteralPath $skill.FullName -Destination $destination -Recurse -Force
    $copied = Get-Item -LiteralPath $destination -Force
    if ($copied.LinkType) {
        Write-Error "Refusing to leave a link at $destination ($($copied.LinkType))"
    }
    $reparse = [System.IO.FileAttributes]::ReparsePoint
    if (($copied.Attributes -band $reparse) -eq $reparse) {
        Write-Error "Refusing to leave a reparse point at $destination"
    }
}
