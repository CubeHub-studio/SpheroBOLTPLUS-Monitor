from __future__ import annotations

import asyncio
import os
from datetime import datetime
from pathlib import Path

from bleak import BleakClient

ADDRESS = os.environ.get("BOLT_ADDRESS")
if not ADDRESS:
    raise SystemExit("Set BOLT_ADDRESS first.")

CHARACTERISTICS = [
    "00010002-574F-4F20-5370-6865726F2121",
    "00010003-574F-4F20-5370-6865726F2121",
]

DEFAULT_LOG = Path.cwd() / "captures" / "bolt_protocol_capture.txt"
LOG_PATH = Path(os.environ.get("BOLT_CAPTURE_LOG", str(DEFAULT_LOG)))


def log(kind: str, message: str) -> None:
    timestamp = datetime.now().isoformat(timespec="milliseconds")
    line = f"[{timestamp}] {kind:<12} {message}"
    print(line, flush=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(line + "\n")


def notification_handler(sender, data: bytearray) -> None:
    raw = bytes(data)
    log("NOTIFY", f"sender={sender} len={len(raw)} data={raw.hex(' ')}")


def disconnected_handler(_client) -> None:
    log("DISCONNECT", "BOLT+ disconnected")


async def main() -> None:
    log("START", f"address={ADDRESS}")
    log("OUTPUT", f"log={LOG_PATH.resolve()}")
    log("INFO", "Passive capture only: this tool does not write commands to the BOLT+.")
    log("INFO", "Change the BOLT+ display with the official software while this runs.")

    client = BleakClient(ADDRESS, disconnected_callback=disconnected_handler)

    try:
        log("CONNECTING", ADDRESS)
        await client.connect()
        log("CONNECTED", f"address={client.address}")

        services = client.services
        log("SERVICES", f"count={len(services.services)}")

        for service in services:
            log("SERVICE", f"uuid={service.uuid}")
            for characteristic in service.characteristics:
                properties = ",".join(characteristic.properties)
                log(
                    "CHAR",
                    f"uuid={characteristic.uuid} properties={properties}",
                )

        for uuid in CHARACTERISTICS:
            log("SUBSCRIBE", uuid)
            await client.start_notify(uuid, notification_handler)

        log("READY", "Listening for notifications. Press Ctrl+C to stop.")

        while client.is_connected:
            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        log("STOP", "Ctrl+C")
    finally:
        if client.is_connected:
            for uuid in CHARACTERISTICS:
                try:
                    await client.stop_notify(uuid)
                except Exception:
                    pass
            await client.disconnect()
        log("DONE", "Capture finished")


if __name__ == "__main__":
    asyncio.run(main())
