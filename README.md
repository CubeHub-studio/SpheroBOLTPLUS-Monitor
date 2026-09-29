# Sphero BOLT+ Monitor

Turn a Sphero BOLT+ into a tiny Windows virtual display.

## Project status

This repository contains the complete project workspace:

- BLE discovery and GATT inspection tools
- BOLT+ BLE connection/notification logger
- 8x8 framebuffer and image-to-LED conversion
- Display bridge process
- Protocol research notes and safe packet-capture workflow
- Windows IddCx virtual-monitor driver scaffold
- Build/install/run helper scripts

The BOLT+ exposes a custom BLE service:

`00010001-574F-4F20-5370-6865726F2121`

with two custom characteristics:

- `00010002-574F-4F20-5370-6865726F2121`
- `00010003-574F-4F20-5370-6865726F2121`

Both were observed to support write and notify operations.

**Important:** the exact BOLT+ application protocol is intentionally not guessed. The current tools can discover, connect, subscribe, and capture traffic without sending arbitrary command packets. Protocol commands should only be added after they are verified.

## Architecture

```
Windows desktop
      |
      v
IddCx virtual display driver
      |
      | desktop swap-chain frames
      v
Sphero display bridge
      |
      | BLE
      v
Sphero BOLT+
      |
      v
8x8 LED matrix
```

The Windows side is based on the Windows Indirect Display Driver model. Microsoft documents IddCx as the user-mode model for monitors that are not connected to a traditional GPU output.

## Requirements

- Windows 11
- Python 3.11+ (Python 3.14 is supported by the bridge code)
- Bluetooth LE adapter
- Sphero BOLT+
- Visual Studio + Windows Driver Kit for the driver portion

Install Python dependencies:

```powershell
py -m pip install -r requirements.txt
```

If `py` is unavailable:

```C:\Python314\python.exe -m pip install -r requirements.txt
```

## Tools

Scan for nearby BLE devices:

```powershell
python tools\bolt_scan.py
```

Inspect the BOLT+ GATT table:

```powershell
python tools\bolt_gatt.py
```

Capture notifications without writing commands:

```powershell
python tools\bolt_logger.py
```

Run the software framebuffer bridge:

```powershell
python bridge\display_bridge.py
```

## BOLT+ address

Do not hard-code a Bluetooth address in source control. Set it at runtime:

```powershell
$env:BOLT_ADDRESS="DE:B4:FA:F9:56:5F"
python bridge\display_bridge.py
```

Replace the address with the one reported by your scanner.

## Virtual monitor

The driver directory is a WDK/IddCx implementation scaffold. It is deliberately kept separate from the Python BLE bridge because Windows supplies desktop frames to the indirect display driver, while Bluetooth communication belongs in the user-mode bridge.

After the driver is functional, Windows should expose a display endpoint named **Sphero BOLT+ Monitor**. The display's physical position can then be configured in Windows Display Settings so it sits to the left of the existing monitor.

## Safety

The BLE logger only subscribes to notifications. It does not send undocumented commands to the robot.

The bridge also refuses to send a BOLT+ LED packet until a verified protocol implementation is supplied.

## License

MIT. See LICENSE.
