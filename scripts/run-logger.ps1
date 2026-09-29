$ErrorActionPreference = "Stop"
if (-not $env:BOLT_ADDRESS) {
    throw "Set BOLT_ADDRESS first."
}
python "$PSScriptRoot\..\tools\bolt_logger.py"
