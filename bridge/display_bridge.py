from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

from .bolt_ble import BoltBLE
from .bolt_protocol import RGB, prepare_display_frame

@dataclass
class DisplayFrame:
    pixels: list[list[RGB]]

def make_test_frame() -> DisplayFrame:
    pixels: list[list[RGB]] = []
    for y in range(8):
        row = []
        for x in range(8):
            row.append(RGB((x * 32) & 255, (y * 32) & 255,
                           ((x + y) * 16) & 255))
        pixels.append(row)
    return DisplayFrame(pixels)

async def main() -> None:
    address = os.environ.get("BOLT_ADDRESS")
    if not address:
        raise SystemExit("Set BOLT_ADDRESS first.")

    print("Sphero BOLT+ display bridge")
    print("Using the BOLT+'s built-in display as the output endpoint.")
    print("BLE connection and display-frame pipeline are ready.")
    print("Display transmission remains disabled until the protocol is verified.")

    bolt = BoltBLE(address)

    try:
        await bolt.connect()
        print("Connected and subscribed to BOLT+ notifications.")

        frame = make_test_frame()
        display_frame = prepare_display_frame(frame.pixels)
        print(f"Prepared BOLT+ display frame: "
              f"{len(display_frame[0])}x{len(display_frame)} RGB pixels.")

        await asyncio.Event().wait()
    finally:
        await bolt.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
