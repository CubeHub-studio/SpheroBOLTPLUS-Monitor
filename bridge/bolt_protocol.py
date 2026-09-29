from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

SERVICE_UUID = "00010001-574F-4F20-5370-6865726F2121"
CHAR_TX_RX_1 = "00010002-574F-4F20-5370-6865726F2121"
CHAR_TX_RX_2 = "00010003-574F-4F20-5370-6865726F2121"

MATRIX_WIDTH = 8
MATRIX_HEIGHT = 8

@dataclass(frozen=True)
class RGB:
    r: int
    g: int
    b: int

    def clipped(self) -> "RGB":
        return RGB(
            max(0, min(255, self.r)),
            max(0, min(255, self.g)),
            max(0, min(255, self.b)),
        )

def resize_to_matrix(pixels: Sequence[Sequence[RGB]], width: int = 8, height: int = 8) -> list[list[RGB]]:
    if not pixels or not pixels[0]:
        return [[RGB(0, 0, 0) for _ in range(width)] for _ in range(height)]

    src_h = len(pixels)
    src_w = len(pixels[0])
    out: list[list[RGB]] = []

    for y in range(height):
        sy = min(src_h - 1, (y * src_h) // height)
        row: list[RGB] = []
        for x in range(width):
            sx = min(src_w - 1, (x * src_w) // width)
            row.append(pixels[sy][sx].clipped())
        out.append(row)

    return out

def flatten_rgb(matrix: Sequence[Sequence[RGB]]) -> bytes:
    data = bytearray()
    for row in matrix:
        for pixel in row:
            p = pixel.clipped()
            data.extend((p.r, p.g, p.b))
    return bytes(data)

def build_led_packet(matrix: Sequence[Sequence[RGB]]) -> bytes:
    """
    Placeholder for the verified BOLT+ LED-matrix protocol.

    This function intentionally raises until the packet format has been
    established from verified protocol documentation or captured Sphero
    application traffic. Sending guessed packets can put the robot into
    an unexpected protocol state.
    """
    raise NotImplementedError(
        "BOLT+ LED packet format is not verified yet. "
        "Capture/verify the Sphero application protocol before enabling BLE writes."
    )
