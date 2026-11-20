param(
    [ValidateSet("all", "full", "frontend", "bio", "comp-bio")]
    [string]$Profile = "full",
    [switch]$DryRun
)

$targetDir = Join-Path $HOME ".gemini\config"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $HOME ".gemini\backup_$timestamp"
$repoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Antigravity Elite Harness Windows Installer ===" -ForegroundColor Cyan
Write-Host "Source:  $repoDir"
Write-Host "Target:  $targetDir"
Write-Host "Profile: $Profile" -ForegroundColor Magenta

# Determine skill categories to install based on profile
$skillSubdirs = @("core")
if ($Profile -in @("all", "full")) {
    $skillSubdirs += @("frontend", "comp-bio")
} elseif ($Profile -eq "frontend") {
    $skillSubdirs += @("frontend")
} elseif ($Profile -in @("bio", "comp-bio")) {
    $skillSubdirs += @("comp-bio")
}

if ($DryRun) {
    Write-Host "[DRY RUN] Would backup $targetDir -> $backupDir" -ForegroundColor Yellow
    Write-Host "[DRY RUN] Would copy hooks, rules, memory, tasks, agents, and skills ($($skillSubdirs -join ', '))" -ForegroundColor Yellow
    Write-Host "[DRY RUN] Verification would run via tests/run-audit.cjs and scripts/validate_skills.py" -ForegroundColor Yellow
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

# Copy skills according to profile
$targetSkillsDir = Join-Path $targetDir "skills"
New-Item -ItemType Directory -Force -Path $targetSkillsDir | Out-Null

foreach ($sub in $skillSubdirs) {
    $srcSub = Join-Path $repoDir "skills\$sub"
    if (Test-Path $srcSub) {
        $destSub = Join-Path $targetSkillsDir $sub
        New-Item -ItemType Directory -Force -Path $destSub | Out-Null
        Copy-Item -Path "$srcSub\*" -Destination $destSub -Recurse -Force
        Write-Host "Installed skill suite: skills/$sub" -ForegroundColor Green
    }
}

Copy-Item -Path "$repoDir\hooks\hooks.json" -Destination "$targetDir\hooks.json" -Force
Copy-Item -Path "$repoDir\SECURITY_ARCHITECTURE.md" -Destination "$targetDir\SECURITY_ARCHITECTURE.md" -Force

Write-Host "Running runtime verification..." -ForegroundColor Cyan
node "$repoDir\tests\run-audit.cjs"
Write-Host "Installation completed successfully with profile '$Profile'." -ForegroundColor Green
