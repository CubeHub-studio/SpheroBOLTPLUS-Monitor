[CmdletBinding()]
param(
    [ValidateSet("Start", "Stop", "Status")]
    [string]$Action = "Start",

    [string]$Output = (Join-Path $PSScriptRoot "..\captures\BthTracing.etl"),

    [switch]$Light
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$CaptureDir = Join-Path $RepoRoot "captures"
$ProfilePath = Join-Path $CaptureDir "BluetoothStack.wprp"
$ProfileUrl = "https://github.com/Microsoft/busiotools/raw/master/bluetooth/tracing/BluetoothStack.wprp"

function Assert-Admin {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)

    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw "Run this script from an elevated PowerShell window (Run as Administrator)."
    }
}

function Get-Profile {
    if (-not (Test-Path $ProfilePath)) {
        New-Item -ItemType Directory -Path $CaptureDir -Force | Out-Null
        Write-Host "Downloading Microsoft's Bluetooth tracing profile..."
        Invoke-WebRequest -Uri $ProfileUrl -OutFile $ProfilePath
    }

    if (-not (Test-Path $ProfilePath)) {
        throw "BluetoothStack.wprp was not downloaded."
    }
}

function Test-Wpr {
    if (-not (Get-Command wpr.exe -ErrorAction SilentlyContinue)) {
        throw "wpr.exe was not found. It is normally included with Windows 11."
    }
}

switch ($Action) {
    "Start" {
        Assert-Admin
        Test-Wpr
        Get-Profile

        New-Item -ItemType Directory -Path $CaptureDir -Force | Out-Null

        $profile = if ($Light) {
            "BluetoothStack.Light"
        } else {
            "BluetoothStack"
        }

        Write-Host ""
        Write-Host "Starting Windows Bluetooth stack capture..."
        Write-Host "Profile: $profile"
        Write-Host "Target device: Sphero BOLT+"
        Write-Host ""
        Write-Host "NEXT:"
        Write-Host "  1. Start Sphero Edu."
        Write-Host "  2. Connect to your BOLT+ (BP-565F)."
        Write-Host "  3. Change something on the BOLT+ built-in display."
        Write-Host "     A display image/text/animation is ideal."
        Write-Host "  4. Leave this capture running until the display command finishes."
        Write-Host "  5. Run this script again with -Action Stop."
        Write-Host ""

        & wpr.exe -start "$ProfilePath!$profile" -filemode

        if ($LASTEXITCODE -ne 0) {
            throw "wpr.exe failed to start the Bluetooth trace. Exit code: $LASTEXITCODE"
        }

        Write-Host "Bluetooth capture is RUNNING."
    }

    "Stop" {
        Assert-Admin
        Test-Wpr

        $resolvedOutput = [IO.Path]::GetFullPath($Output)

        New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($resolvedOutput)) -Force | Out-Null

        Write-Host "Stopping Bluetooth capture..."
        & wpr.exe -stop "$resolvedOutput"

        if ($LASTEXITCODE -ne 0) {
            throw "wpr.exe failed to stop the Bluetooth trace. Exit code: $LASTEXITCODE"
        }

        Write-Host ""
        Write-Host "Capture saved to:"
        Write-Host "  $resolvedOutput"
        Write-Host ""
        Write-Host "This ETL contains Windows Bluetooth stack tracing."
        Write-Host "Use Microsoft's BTETLParse.exe from the Bluetooth Test Platform"
        Write-Host "to extract HCI traces from supported ETL files."
    }

    "Status" {
        Test-Wpr
        & wpr.exe -status
    }
}
