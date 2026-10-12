# Adds the forge to an existing muse-local-gateway install (Windows).
#   .\install.ps1 ..\muse-local-gateway            add
#   .\install.ps1 ..\muse-local-gateway -Remove    back to the plain bench
# ASCII only: Windows PowerShell reads .ps1 files as ANSI.
param([Parameter(Mandatory)][string]$Gateway, [switch]$Remove)
$ErrorActionPreference = 'Stop'
$gw = (Resolve-Path $Gateway).Path
$envFile = Join-Path $gw '.env'
if (-not (Test-Path $envFile)) { throw "set up muse-local-gateway first ($envFile not found)" }
$forge = Join-Path $PSScriptRoot 'compose.forge.yaml'

$lines = Get-Content $envFile
$i = [array]::FindIndex([string[]]$lines, [Predicate[string]]{ param($l) $l -like 'COMPOSE_FILE=*' })
if ($i -lt 0) { throw "no COMPOSE_FILE in $envFile" }
$files = @($lines[$i].Substring(13) -split ';' | Where-Object { $_ -and $_ -notlike '*compose.forge.yaml' })
if (-not $Remove) { $files += $forge }
$lines[$i] = 'COMPOSE_FILE=' + ($files -join ';')
# Write in place so .env keeps its restricted permissions (it holds the Tailscale key).
[IO.File]::WriteAllText($envFile, (($lines -join "`n") + "`n"))

if (-not ($files -match 'compose.usb.yaml')) { Write-Host 'Note: USB serial is off in the gateway. Re-run its setup (delete .env first) and answer y to USB.' }
Write-Host 'Pulling ESP-IDF (about 5 GB the first time)...'
Push-Location $gw
try {
  docker compose up -d; if ($LASTEXITCODE) { throw 'docker compose up failed' }
  docker compose exec -T bench idf.py --version; if ($LASTEXITCODE) { throw 'bench did not come up with ESP-IDF' }
} finally { Pop-Location }
