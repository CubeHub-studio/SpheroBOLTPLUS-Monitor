from __future__ import annotations

import asyncio
from collections.abc import Callable
from bleak import BleakClient

from .bolt_protocol import CHAR_TX_RX_1, CHAR_TX_RX_2, build_led_packet

NotificationCallback = Callable[[str, bytes], None]

class BoltBLE:
    def __init__(self, address: str, on_notification: NotificationCallback | None = None):
        self.address = address
        self.on_notification = on_notification
        self.client: BleakClient | None = None

    def _notify(self, sender, data: bytearray) -> None:
        if self.on_notification:
            self.on_notification(str(sender), bytes(data))

    async def connect(self) -> None:
        self.client = BleakClient(self.address)
        await self.client.connect()

        await self.client.start_notify(CHAR_TX_RX_1, self._notify)
        await self.client.start_notify(CHAR_TX_RX_2, self._notify)

    async def disconnect(self) -> None:
        if not self.client:
            return

        for uuid in (CHAR_TX_RX_1, CHAR_TX_RX_2):
            try:
                await self.client.stop_notify(uuid)
            except Exception:
                pass

        if self.client.is_connected:
            await self.client.disconnect()

    async def send_matrix(self, matrix) -> None:
        if not self.client or not self.client.is_connected:
            raise RuntimeError("BOLT+ is not connected")

        packet = build_led_packet(matrix)

        # Protocol selection will be implemented once the packet format is verified.
        await self.client.write_gatt_char(CHAR_TX_RX_1, packet, response=False)
