param(
    [switch]$DryRun
)

$targetDir = Join-Path $HOME ".gemini\config"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $HOME ".gemini\backup_$timestamp"
$repoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Antigravity Elite Harness Windows Installer ===" -ForegroundColor Cyan
Write-Host "Source: $repoDir"
Write-Host "Target: $targetDir"

if ($DryRun) {
    Write-Host "[DRY RUN] Would backup $targetDir -> $backupDir" -ForegroundColor Yellow
    Write-Host "[DRY RUN] Would copy hooks, rules, memory, and tasks into $targetDir" -ForegroundColor Yellow
    Write-Host "[DRY RUN] Verification would run via tests/run-audit.cjs" -ForegroundColor Yellow
    return
}

if (Test-Path $targetDir) {
    Write-Host "Creating safety backup at $backupDir..." -ForegroundColor Green
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    Copy-Item -Path "$targetDir\*" -Destination $backupDir -Recurse -Force
}

$dirs = @("hooks", "rules", "memory", "tasks", "agents")
foreach ($d in $dirs) {
    $dest = Join-Path $targetDir $d
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Path "$repoDir\$d\*" -Destination $dest -Recurse -Force
}

Copy-Item -Path "$repoDir\hooks\hooks.json" -Destination "$targetDir\hooks.json" -Force
Copy-Item -Path "$repoDir\SECURITY_ARCHITECTURE.md" -Destination "$targetDir\SECURITY_ARCHITECTURE.md" -Force

Write-Host "Running runtime verification..." -ForegroundColor Cyan
node "$repoDir\tests\run-audit.cjs"
Write-Host "Installation completed successfully." -ForegroundColor Green
