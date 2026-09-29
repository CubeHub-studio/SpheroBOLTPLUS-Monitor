# BOLT+ protocol research

The BOLT+ currently exposes these observed UUIDs:

- Service: `00010001-574F-4F20-5370-6865726F2121`
- Characteristic: `00010002-574F-4F20-5370-6865726F2121`
- Characteristic: `00010003-574F-4F20-5370-6865726F2121`

Both characteristics advertise write and notify capabilities.

The passive connection test showed that Windows can connect and subscribe to the characteristics. The BOLT+ changed its LED state during the connection/subscription session, but no notifications were observed without application-level initialization.

## Protocol discovery plan

1. Keep the passive logger running.
2. Connect the BOLT+ using the official Sphero application.
3. Capture traffic using a Bluetooth protocol analyzer if available.
4. Record packet direction, characteristic, timestamp, and payload.
5. Repeat the same operation several times with controlled changes.
6. Identify framing, command IDs, sequence fields, checksums, and response packets.
7. Implement only commands confirmed by multiple observations.

Do not send random packets to the robot while reverse-engineering.

## Matrix format

The software side represents the LED display as an 8x8 matrix of RGB pixels. The protocol adapter is deliberately isolated in `bridge/bolt_protocol.py`.

Once the verified command format is known, only the packet builder and connection initialization need to change. The Windows display and framebuffer layers can remain independent.
