import asyncio
from open_gopro import WirelessGoPro

async def main() -> None:

    async with WirelessGoPro() as gopro:
        print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
        # Send some messages now

if __name__ == "__main__":
    asyncio.run(main())