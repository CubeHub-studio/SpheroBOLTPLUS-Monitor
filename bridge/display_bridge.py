from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

from .bolt_ble import BoltBLE
from .bolt_protocol import (
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    RGB,
    prepare_display_frame,
)


@dataclass
class DisplayFrame:
    pixels: list[list[RGB]]


def make_test_frame() -> DisplayFrame:
    """Create a 128x128 RGB test frame for the BOLT+ LCD."""

    pixels: list[list[RGB]] = []

    for y in range(DISPLAY_HEIGHT):
        row: list[RGB] = []

        for x in range(DISPLAY_WIDTH):
            row.append(
                RGB(
                    (x * 255) // (DISPLAY_WIDTH - 1),
                    (y * 255) // (DISPLAY_HEIGHT - 1),
                    ((x + y) * 255) // (DISPLAY_WIDTH + DISPLAY_HEIGHT - 2),
                )
            )

        pixels.append(row)

    return DisplayFrame(pixels)


async def main() -> None:
    address = os.environ.get("BOLT_ADDRESS")

    if not address:
        raise SystemExit("Set BOLT_ADDRESS first.")

    print("Sphero BOLT+ display bridge")
    print("Output endpoint: BOLT+ built-in 128x128 LCD.")
    print("BLE transport is ready.")
    print("LCD command transmission remains disabled until its DID/CID")
    print("and payload format are verified.")

    bolt = BoltBLE(address)

    try:
        await bolt.connect()
        print("Connected and subscribed to BOLT+ notifications.")

        frame = make_test_frame()
        display_frame = prepare_display_frame(frame.pixels)

        print(
            f"Prepared display frame: "
            f"{len(display_frame[0])}x{len(display_frame)} RGB pixels."
        )

        await asyncio.Event().wait()

    finally:
        await bolt.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
