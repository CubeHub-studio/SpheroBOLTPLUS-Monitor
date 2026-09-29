import asyncio
import os
from bleak import BleakClient

ADDRESS = os.environ.get("BOLT_ADDRESS")
if not ADDRESS:
    raise SystemExit("Set BOLT_ADDRESS first, for example: $env:BOLT_ADDRESS='DE:B4:FA:F9:56:5F'")

async def main() -> None:
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        for service in client.services:
            print("\nSERVICE")
            print(f"UUID: {service.uuid}")
            print(f"Description: {service.description}")
            for char in service.characteristics:
                print(f"  {char.uuid}")
                print(f"    {char.description}")
                print(f"    properties: {', '.join(char.properties)}")
                for descriptor in char.descriptors:
                    print(f"    descriptor: {descriptor.uuid}")

if __name__ == "__main__":
    asyncio.run(main())
