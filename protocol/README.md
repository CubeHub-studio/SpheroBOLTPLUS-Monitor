# BOLT+ display protocol research

This project targets the **actual display built into the Sphero BOLT+**.

Observed BLE service:

- `00010001-574F-4F20-5370-6865726F2121`

Observed characteristics:

- `00010002-574F-4F20-5370-6865726F2121`
- `00010003-574F-4F20-5370-6865726F2121`

Both advertise write and notify capabilities.

## Current observation

A passive Windows connection can subscribe to both characteristics. The BOLT+ changes its visible state during the connection/subscription session, but no notification payloads were observed without application-level initialization.

## Goal

The protocol adapter must eventually send frames to the BOLT+'s real built-in display.

The display pipeline should be:

1. Windows produces a desktop frame.
2. The virtual display driver passes the frame to the bridge.
3. The bridge converts the frame to the BOLT+'s native display dimensions.
4. The verified BOLT+ display protocol encodes the frame.
5. BLE sends the encoded display command to the BOLT+.

No guessed packet format should be used.

## Protocol discovery

1. Run the passive logger.
2. Use the official Sphero application and perform a known display-related action.
3. Capture BLE traffic with an appropriate Bluetooth analyzer.
4. Record characteristic, direction, timestamp, and payload.
5. Repeat controlled actions.
6. Identify framing, command IDs, sequence fields, checksums, and acknowledgements.
7. Implement only confirmed commands.

The protocol implementation belongs in `bridge/bolt_protocol.py`, keeping it independent from the Windows display driver.
