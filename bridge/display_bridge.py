from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

from .bolt_ble import BoltBLE
from .bolt_protocol import RGB, resize_to_matrix

@dataclass
class Frame:
    pixels: list[list[RGB]]

def make_test_frame() -> Frame:
    pixels: list[list[RGB]] = []
    for y in range(8):
        row = []
        for x in range(8):
            row.append(
                RGB(
                    r=(x * 32) & 255,
                    g=(y * 32) & 255,
                    b=((x + y) * 16) & 255,
                )
            )
        pixels.append(row)
    return Frame(pixels)

async def main() -> None:
    address = os.environ.get("BOLT_ADDRESS")
    if not address:
        raise SystemExit("Set BOLT_ADDRESS first.")

    print("Sphero BOLT+ display bridge")
    print("BLE connection and framebuffer pipeline are ready.")
    print("LED transmission remains disabled until the protocol is verified.")

    bolt = BoltBLE(address)

    try:
        await bolt.connect()
        print("Connected and subscribed to BOLT+ notifications.")

        frame = make_test_frame()
        matrix = resize_to_matrix(frame.pixels)
        print(f"Prepared {len(matrix)}x{len(matrix[0])} RGB framebuffer.")

        # Deliberately do not call send_matrix yet.
        await asyncio.Event().wait()
    finally:
        await bolt.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
