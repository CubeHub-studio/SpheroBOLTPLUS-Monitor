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

LOG_PATH = Path(os.environ.get("BOLT_LOG", str(Path.home() / "bolt_ble_log.txt")))

def log(message: str) -> None:
    line = f"[{datetime.now().isoformat(timespec='milliseconds')}] {message}"
    print(line)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def notification_handler(sender, data: bytearray) -> None:
    log(f"NOTIFY | {sender} | {bytes(data).hex(' ')}")

async def main() -> None:
    log(f"CONNECTING | {ADDRESS}")
    async with BleakClient(ADDRESS) as client:
        log(f"CONNECTED | {client.address}")

        for uuid in CHARACTERISTICS:
            log(f"SUBSCRIBE | {uuid}")
            await client.start_notify(uuid, notification_handler)

        log("LISTENING | Ctrl+C to stop")

        try:
            while client.is_connected:
                await asyncio.sleep(0.1)
        finally:
            for uuid in CHARACTERISTICS:
                try:
                    await client.stop_notify(uuid)
                except Exception:
                    pass
            log("DISCONNECTED")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
