# Sphero BOLT+ Monitor

Turn the **actual BOLT+ display** into a Windows virtual display.

## Project status

This repository contains:
- BLE discovery and GATT inspection tools
- BOLT+ BLE connection/notification logger
- display framebuffer pipeline
- BOLT+ display protocol adapter
- Windows IddCx virtual-display driver scaffold
- build/install/run helpers

The BOLT+ exposes this custom BLE service:

`00010001-574F-4F20-5370-6865726F2121`

with these two characteristics:

- `00010002-574F-4F20-5370-6865726F2121`
- `00010003-574F-4F20-5370-6865726F2121`

Both were observed to support write and notify operations.

**Important:** the exact BOLT+ application protocol is not guessed. The current tools can discover, connect, subscribe, and capture traffic without sending undocumented commands.

## Architecture

```
Windows desktop
      |
      v
IddCx virtual display driver
      |
      | desktop frame
      v
Display bridge
      |
      | BLE
      v
Sphero BOLT+
      |
      v
BOLT+ built-in display
```

The project treats the BOLT+'s built-in display as the physical display endpoint. It does not create a separate software LED matrix abstraction.

## Requirements

- Windows 11
- Python 3.11+
- Bluetooth LE adapter
- Sphero BOLT+
- Visual Studio + Windows Driver Kit for the driver

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Set the address at runtime:

```powershell
$env:BOLT_ADDRESS="XX:XX:XX:XX:XX:XX"
```

Scan:

```powershell
python tools\bolt_scan.py
```

Inspect GATT:

```powershell
python tools\bolt_gatt.py
```

Capture notifications:

```powershell
python tools\bolt_logger.py
```

Run the bridge:

```powershell
python bridge\display_bridge.py
```

## Windows display position

Once the IddCx driver is functional, Windows will see **Sphero BOLT+ Monitor** as another display. Windows Display Settings can place that display to the **left** of the existing physical monitor.

## Safety

The BLE logger only subscribes to notifications. It does not send undocumented commands.

The display bridge refuses to transmit display data until the verified BOLT+ display protocol has been implemented.

See `protocol/README.md` and `driver/README.md`.
