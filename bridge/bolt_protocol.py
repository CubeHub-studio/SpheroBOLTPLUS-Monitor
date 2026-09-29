from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

# Sphero V2 packet framing.
SOP = 0x8D
EOP = 0xD8
ESC = 0xAB
ESC_ESC = 0x23
ESC_SOP = 0x05
ESC_EOP = 0x50

# Standard Sphero V2 command flags.
FLAG_REQUESTS_RESPONSE = 0x02
FLAG_RESETS_INACTIVITY_TIMEOUT = 0x08

SERVICE_UUID = "00010001-574F-4F20-5370-6865726F2121"
CHAR_TX_RX_1 = "00010002-574F-4F20-5370-6865726F2121"
CHAR_TX_RX_2 = "00010003-574F-4F20-5370-6865726F2121"

# The physical BOLT+ LCD is 128x128 pixels.
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 128


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


def prepare_display_frame(
    pixels: Sequence[Sequence[RGB]],
    width: int = DISPLAY_WIDTH,
    height: int = DISPLAY_HEIGHT,
) -> list[list[RGB]]:
    """Resize a source frame to the BOLT+ built-in LCD dimensions."""

    if width <= 0 or height <= 0:
        raise ValueError("Display dimensions must be positive.")

    if not pixels or not pixels[0]:
        black = RGB(0, 0, 0)
        return [[black for _ in range(width)] for _ in range(height)]

    src_h = len(pixels)
    src_w = len(pixels[0])

    if any(len(row) != src_w for row in pixels):
        raise ValueError("Display frame rows must all have the same width.")

    result: list[list[RGB]] = []

    for y in range(height):
        sy = min(src_h - 1, (y * src_h) // height)
        row: list[RGB] = []

        for x in range(width):
            sx = min(src_w - 1, (x * src_w) // width)
            row.append(pixels[sy][sx].clipped())

        result.append(row)

    return result


def _escape(data: Sequence[int]) -> bytes:
    """Apply Sphero V2 SLIP-style escaping to a packet body."""

    output = bytearray()

    for value in data:
        value &= 0xFF

        if value == ESC:
            output.extend((ESC, ESC_ESC))
        elif value == SOP:
            output.extend((ESC, ESC_SOP))
        elif value == EOP:
            output.extend((ESC, ESC_EOP))
        else:
            output.append(value)

    return bytes(output)


def sphero_checksum(data: Sequence[int]) -> int:
    """Sphero V2 checksum: one's complement of the byte sum."""

    return (~sum(data)) & 0xFF


def build_sphero_command(
    device_id: int,
    command_id: int,
    payload: Sequence[int] = (),
    *,
    sequence: int = 0,
    requests_response: bool = True,
) -> bytes:
    """Build a standard Sphero V2 command packet.

    This implements the documented transport framing. It does not guess
    which DID/CID corresponds to a BOLT+ LCD operation.
    """

    flags = FLAG_RESETS_INACTIVITY_TIMEOUT
    if requests_response:
        flags |= FLAG_REQUESTS_RESPONSE

    body = bytearray(
        (
            flags,
            device_id & 0xFF,
            command_id & 0xFF,
            sequence & 0xFF,
        )
    )
    body.extend(value & 0xFF for value in payload)
    body.append(sphero_checksum(body))

    return bytes((SOP,)) + _escape(body) + bytes((EOP,))


def build_display_packet(frame: Sequence[Sequence[RGB]]) -> bytes:
    """Build a BOLT+ LCD display packet.

    The LCD is 128x128. The actual BOLT+ LCD command DID/CID and payload
    format are intentionally not hard-coded until they are verified from
    Sphero documentation or captured official-app traffic.
    """

    raise NotImplementedError(
        "The BOLT+ LCD command format still needs to be verified. "
        "The Sphero V2 transport layer is now implemented."
    )
