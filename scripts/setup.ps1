$ErrorActionPreference = "Stop"

Write-Host "Installing Python dependencies..."
python -m pip install -r "$PSScriptRoot\..\requirements.txt"

Write-Host ""
Write-Host "Setup complete."
Write-Host "Set your BOLT+ address with:"
Write-Host '  $env:BOLT_ADDRESS="XX:XX:XX:XX:XX:XX"'
Write-Host "Then run:"
Write-Host "  python bridge\display_bridge.py"
