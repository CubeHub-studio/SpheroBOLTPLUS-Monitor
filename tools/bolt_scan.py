import asyncio
from bleak import BleakScanner

async def main() -> None:
    print("Scanning for BLE devices for 15 seconds...")
    devices = await BleakScanner.discover(timeout=15, return_adv=True)

    for device, advertisement in devices.values():
        name = device.name or advertisement.local_name or "<unnamed>"
        print(f"Name: {name}")
        print(f"Address: {device.address}")
        print(f"RSSI: {getattr(advertisement, 'rssi', 'unknown')}")
        for uuid in advertisement.service_uuids or []:
            print(f"  Service UUID: {uuid}")
        print()

if __name__ == "__main__":
    asyncio.run(main())
