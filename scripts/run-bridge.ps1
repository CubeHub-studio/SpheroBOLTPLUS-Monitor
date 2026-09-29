$ErrorActionPreference = "Stop"
if (-not $env:BOLT_ADDRESS) {
    throw "Set BOLT_ADDRESS first."
}
python "$PSScriptRoot\..\bridge\display_bridge.py"
