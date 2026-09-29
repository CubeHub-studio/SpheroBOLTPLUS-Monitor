from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

SERVICE_UUID = "00010001-574F-4F20-5370-6865726F2121"
CHAR_TX_RX_1 = "00010002-574F-4F20-5370-6865726F2121"
CHAR_TX_RX_2 = "00010003-574F-4F20-5370-6865726F2121"

DISPLAY_WIDTH = 8
DISPLAY_HEIGHT = 8

@dataclass(frozen=True)
class RGB:
    r: int
    g: int
    b: int

    def clipped(self) -> "RGB":
        return RGB(max(0, min(255, self.r)),
                   max(0, min(255, self.g)),
                   max(0, min(255, self.b)))

def prepare_display_frame(pixels: Sequence[Sequence[RGB]],
                          width: int = DISPLAY_WIDTH,
                          height: int = DISPLAY_HEIGHT) -> list[list[RGB]]:
    """Prepare a frame for the BOLT+ built-in display.

    This represents the physical display endpoint, not a separate matrix
    device. The protocol adapter will map these pixels to the verified
    BOLT+ display command format.
    """
    if not pixels or not pixels[0]:
        return [[RGB(0, 0, 0) for _ in range(width)] for _ in range(height)]

    src_h = len(pixels)
    src_w = len(pixels[0])
    result: list[list[RGB]] = []

    for y in range(height):
        sy = min(src_h - 1, (y * src_h) // height)
        row: list[RGB] = []
        for x in range(width):
            sx = min(src_w - 1, (x * src_w) // width)
            row.append(pixels[sy][sx].clipped())
        result.append(row)

    return result

def build_display_packet(frame: Sequence[Sequence[RGB]]) -> bytes:
    """Build a verified BOLT+ display packet.

    Disabled until the real BOLT+ display protocol is verified from
    documentation or captured official-app traffic.
    """
    raise NotImplementedError(
        "BOLT+ display packet format is not verified yet. "
        "Capture/verify the Sphero display protocol before enabling BLE writes."
    )
