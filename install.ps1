param(
    [ValidateSet("all", "full", "frontend", "bio", "comp-bio")]
    [string]$Profile = "full",
    [switch]$DryRun,
    [switch]$Uninstall,
    [switch]$AllRules
)

$targetDir = Join-Path $HOME ".gemini\config"
$repoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Uninstall) {
    Write-Host "=== Uninstalling Antigravity Elite Harness ===" -ForegroundColor Yellow
    Write-Host "Target: $targetDir"

    # Remove installed harness component directories
    $dirs = @("hooks", "memory", "tasks", "agents")
    foreach ($d in $dirs) {
        $path = Join-Path $targetDir $d
        if (Test-Path $path) {
            Write-Host "Removing $path..." -ForegroundColor Gray
            Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    # Remove installed harness skills
    $targetSkillsDir = Join-Path $targetDir "skills"
    if (Test-Path $targetSkillsDir) {
        $skillSubs = @("core", "frontend", "comp-bio")
        foreach ($sub in $skillSubs) {
            $srcSub = Join-Path $repoDir "skills\$sub"
            if (Test-Path $srcSub) {
                Get-ChildItem -Directory $srcSub | ForEach-Object {
                    $skillDest = Join-Path $targetSkillsDir $_.Name
                    if (Test-Path $skillDest) {
                        Write-Host "Removing skill: $skillDest..." -ForegroundColor Gray
                        Remove-Item -Path $skillDest -Recurse -Force -ErrorAction SilentlyContinue
                    }
                }
            }
        }
    }

    # Remove top-level configuration artifacts
    Remove-Item (Join-Path $targetDir "hooks.json") -Force -ErrorAction SilentlyContinue
    Remove-Item (Join-Path $targetDir "SECURITY_ARCHITECTURE.md") -Force -ErrorAction SilentlyContinue
    Remove-Item (Join-Path $targetDir "rules\global-core.md") -Force -ErrorAction SilentlyContinue

    # Restore from latest backup if available
    $geminiDir = Join-Path $HOME ".gemini"
    $latestBackup = Get-ChildItem -Path $geminiDir -Directory -Filter "backup_*" | 
                    Sort-Object CreationTime -Descending | 
                    Select-Object -First 1

    if ($latestBackup) {
        Write-Host "Restoring previous configuration from $($latestBackup.FullName)..." -ForegroundColor Green
        Copy-Item -Path "$($latestBackup.FullName)\*" -Destination $targetDir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Restoration complete." -ForegroundColor Green
    } else {
        Write-Host "No prior backup directory found." -ForegroundColor Gray
    }

    Write-Host "Uninstallation finished cleanly." -ForegroundColor Green
    return
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $HOME ".gemini\backup_$timestamp"

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
    Write-Host "[DRY RUN] Verification would run via npm run verify" -ForegroundColor Yellow
    return
}

if (Test-Path $targetDir) {
    Write-Host "Creating safety backup at $backupDir..." -ForegroundColor Green
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    Copy-Item -Path "$targetDir\*" -Destination $backupDir -Recurse -Force
}

$dirs = @("hooks", "memory", "tasks", "agents")
foreach ($d in $dirs) {
    $dest = Join-Path $targetDir $d
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Path "$repoDir\$d\*" -Destination $dest -Recurse -Force
}

$rulesDest = Join-Path $targetDir "rules"
New-Item -ItemType Directory -Force -Path $rulesDest | Out-Null
if ($AllRules) {
    Copy-Item -Path "$repoDir\rules\*" -Destination $rulesDest -Recurse -Force
} else {
    Copy-Item -Path "$repoDir\rules\global-core.md" -Destination (Join-Path $rulesDest "global-core.md") -Force
}

# Copy skills according to profile directly into target skills root so Antigravity discovers them
$targetSkillsDir = Join-Path $targetDir "skills"
New-Item -ItemType Directory -Force -Path $targetSkillsDir | Out-Null

foreach ($sub in $skillSubdirs) {
    $srcSub = Join-Path $repoDir "skills\$sub"
    if (Test-Path $srcSub) {
        Get-ChildItem -Directory $srcSub | ForEach-Object {
            $skillName = $_.Name
            $destSkill = Join-Path $targetSkillsDir $skillName
            New-Item -ItemType Directory -Force -Path $destSkill | Out-Null
            Copy-Item -Path "$($_.FullName)\*" -Destination $destSkill -Recurse -Force
            Write-Host "Installed skill: $skillName (from $sub)" -ForegroundColor Green
        }
    }
}

$targetDirPosix = $targetDir -replace '\\', '/'
$hooksJson = Get-Content "$repoDir\hooks\hooks.json" -Raw -Encoding UTF8
$hooksJson = $hooksJson -replace 'node hooks/([a-zA-Z0-9._-]+)', "node \`"$targetDirPosix/hooks/`$1\`""
[System.IO.File]::WriteAllText((Join-Path $targetDir "hooks.json"), $hooksJson, (New-Object System.Text.UTF8Encoding $false))
if (Test-Path "$repoDir\docs\security-architecture.md") {
    Copy-Item -Path "$repoDir\docs\security-architecture.md" -Destination "$targetDir\SECURITY_ARCHITECTURE.md" -Force
}

Write-Host "Running runtime verification..." -ForegroundColor Cyan
node "$repoDir\tests\run-audit.cjs"
Write-Host "Installation completed successfully with profile '$Profile'." -ForegroundColor Green
