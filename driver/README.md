# Windows virtual display driver

This directory contains the BOLT+ IddCx driver layer.

## Display endpoint

The driver exposes one virtual monitor named:

**Sphero BOLT+ Monitor**

That monitor represents the **actual display built into the BOLT+**. There is no separate virtual LED-matrix device.

Windows desktop frames arrive through IddCx. The driver/bridge pipeline will convert those frames to the native BOLT+ display format and transmit them over BLE.

## Architecture

```
Windows compositor
      |
      v
IddCx swap chain
      |
      v
BOLT+ Monitor driver
      |
      | IPC
      v
Display bridge
      |
      | Bluetooth LE
      v
Sphero BOLT+ built-in display
```

The driver must not directly depend on Python or the BLE implementation.

## Current state

This is a WDK/IddCx scaffold. The production implementation still needs monitor enumeration, supported modes, swap-chain processing, IPC, INF/device installation, signing, and lifecycle handling.

Use Microsoft's current IddSampleDriver as the implementation reference.
