<#
.SYNOPSIS
    Local Port Guard & Allocator Utility.
    Manages assigned ports and prevents collisions across local development projects.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("list", "check", "next", "register", "kill")]
    [string]$Action = "list",

    [Parameter()]
    [int]$Port = 0,

    [Parameter()]
    [ValidateSet("desktop", "web", "automation", "media")]
    [string]$Category = "desktop",

    [Parameter()]
    [string]$ProjectName = "",

    [Parameter()]
    [string]$ProjectPath = "",

    [Parameter()]
    [string]$ServiceType = "Custom Server"
)

$registryPath = "$HOME\.gemini\config\local-ports-registry.json"
$markdownPath = "$HOME\.gemini\config\LOCAL_PORTS_DIRECTORY.md"

if (-not (Test-Path $registryPath)) {
    Write-Error "Registry file not found at: $registryPath"
    exit 1
}

$registry = Get-Content $registryPath -Raw | ConvertFrom-Json

function Test-PortListening([int]$p) {
    $conn = Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue
    return ($null -ne $conn)
}

function Get-PortProcess([int]$p) {
    $conn = Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($conn) {
        $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        return [PSCustomObject]@{
            PID  = $conn.OwningProcess
            Name = if ($proc) { $proc.ProcessName } else { "Unknown" }
        }
    }
    return $null
}

switch ($Action) {
    "list" {
        Write-Host "`n=== [ LOCAL PORTS REGISTRY & STATUS ] ===" -ForegroundColor Cyan
        
        Write-Host "`n[Allocated Projects]:" -ForegroundColor Yellow
        $projectList = @()
        foreach ($item in $registry.allocated_projects) {
            $isLive = Test-PortListening $item.port
            $procInfo = if ($isLive) { Get-PortProcess $item.port } else { $null }
            $statusText = if ($isLive) { "ACTIVE (PID: $($procInfo.PID) - $($procInfo.Name))" } else { "Offline (Reserved)" }
            $statusColor = if ($isLive) { "Green" } else { "Gray" }

            $projectList += [PSCustomObject]@{
                Port        = $item.port
                Project     = $item.project_name
                Category    = $item.category
                Type        = $item.type
                SystemState = $statusText
            }
        }
        $projectList | Format-Table -AutoSize

        Write-Host "`n[Common & System Reserved Ports]:" -ForegroundColor Yellow
        $sysList = @()
        foreach ($item in $registry.reserved_system_ports) {
            $isLive = Test-PortListening $item.port
            $sysList += [PSCustomObject]@{
                Port     = $item.port
                Name     = $item.name
                Category = $item.category
                IsActive = if ($isLive) { "YES (Listening)" } else { "No" }
            }
        }
        $sysList | Format-Table -AutoSize
    }

    "check" {
        if ($Port -le 0) {
            Write-Host "Please specify -Port <number>" -ForegroundColor Red
            exit 1
        }

        Write-Host "`nChecking Port $Port..." -ForegroundColor Cyan
        $allocated = $registry.allocated_projects | Where-Object { $_.port -eq $Port }
        $reserved = $registry.reserved_system_ports | Where-Object { $_.port -eq $Port }
        $procInfo = Get-PortProcess $Port

        if ($allocated) {
            Write-Host "[RESERVED] Port $Port is registered to project: '$($allocated.project_name)'" -ForegroundColor Red
            Write-Host "Path: $($allocated.path)" -ForegroundColor Gray
        } elseif ($reserved) {
            Write-Host "[RESERVED] Port $Port is registered as system/framework port: '$($reserved.name)'" -ForegroundColor Red
        } else {
            Write-Host "[AVAILABLE IN REGISTRY] Port $Port is not registered to any project." -ForegroundColor Green
        }

        if ($procInfo) {
            Write-Host "[SYSTEM STATE] Port is CURRENTLY LISTENING by process: $($procInfo.Name) (PID: $($procInfo.PID))" -ForegroundColor Yellow
        } else {
            Write-Host "[SYSTEM STATE] Port is completely free on the network right now." -ForegroundColor Green
        }
    }

    "next" {
        $categoryKey = switch ($Category) {
            "desktop"    { "desktop_electron_backends" }
            "web"        { "web_fullstack_servers" }
            "automation" { "automation_tools_mcp" }
            "media"      { "media_streaming_websocket" }
            default      { "desktop_electron_backends" }
        }

        $range = $registry.ranges.$categoryKey
        $start = [int]$range.start
        $end = [int]$range.end

        $usedPorts = @()
        $registry.allocated_projects | ForEach-Object { $usedPorts += [int]$_.port }
        $registry.reserved_system_ports | ForEach-Object { $usedPorts += [int]$_.port }

        $candidate = $start
        while ($candidate -le $end) {
            if ($candidate -notin $usedPorts) {
                # Check live system
                if (-not (Test-PortListening $candidate)) {
                    break
                }
            }
            $candidate++
        }

        if ($candidate -gt $end) {
            Write-Error "No free ports found in range $start - $end!"
            exit 1
        }

        Write-Host "`n[RECOMMENDED NEXT FREE PORT] --> $candidate" -ForegroundColor Green
        Write-Host "Category: $categoryKey ($($range.description))`n" -ForegroundColor Cyan

        if (-not [string]::IsNullOrWhiteSpace($ProjectName)) {
            Write-Host "Registering '$ProjectName' with port $candidate..." -ForegroundColor Yellow
            $newEntry = [PSCustomObject]@{
                port          = $candidate
                project_name  = $ProjectName
                path          = if ($ProjectPath) { $ProjectPath } else { "Pending" }
                category      = $categoryKey
                type          = $ServiceType
                status        = "active"
                assigned_date = (Get-Date -Format "yyyy-MM-dd")
                notes         = "Allocated via port-guard CLI"
            }
            $registry.allocated_projects += $newEntry
            $registry | ConvertTo-Json -Depth 10 | Set-Content $registryPath -Encoding UTF8
            Write-Host "Successfully registered port $candidate in local-ports-registry.json!" -ForegroundColor Green
        }
    }

    "kill" {
        if ($Port -le 0) {
            Write-Host "Please specify -Port <number> to terminate process." -ForegroundColor Red
            exit 1
        }
        $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -eq $conn) {
            Write-Host "No active listener found on port $Port." -ForegroundColor Green
        } else {
            $pidToKill = $conn.OwningProcess
            $proc = Get-Process -Id $pidToKill -ErrorAction SilentlyContinue
            Write-Host "Killing process '$($proc.ProcessName)' (PID: $pidToKill) on port $Port..." -ForegroundColor Yellow
            Stop-Process -Id $pidToKill -Force
            Write-Host "Port $Port released successfully!" -ForegroundColor Green
        }
    }
}


