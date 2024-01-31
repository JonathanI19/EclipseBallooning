import asyncio
from open_gopro import WirelessGoPro, Params, proto

async def main() -> None:

    async with WirelessGoPro() as gopro:
        print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
        
        # String value
        print(gopro.version)

        # Bool values
        print(gopro.is_ble_connected)
        print(gopro.is_http_connected)
        print(gopro.is_open)

        # Get JSON data of all gopro statuses
        # status = await gopro.http_command.get_camera_state()
        # print(status)
        
        # Getting media list before recording
        media_set_before = set((await gopro.http_command.get_media_list()).data.files)
        
        # # Start recording
        # print("Attempting to capture video")
        # assert (await gopro.http_command.set_shutter(shutter=Params.Toggle.ENABLE)).ok

        # # Sleep for 10 seconds
        # await asyncio.sleep(10.0)

        # # Stop recording
        # assert (await gopro.http_command.set_shutter(shutter=Params.Toggle.DISABLE)).ok

        # Lets try streaming:
        print("Attempting to stream")
        assert (await gopro.http_command.set_preview_stream(mode=Params.Toggle.ENABLE)).ok

        print("Sleeping while recording")
        await asyncio.sleep(30.0)

        assert (await gopro.http_command.set_preview_stream(mode=Params.Toggle.DISABLE)).ok
        print("Done Streaming")

        # Get media list after recording
        media_set_after = set((await gopro.http_command.get_media_list()).data.files)

        # Pop the difference and download - May not always be the difference
        video = media_set_after.difference(media_set_before).pop()
        print("Downloading...")
        await gopro.http_command.download_file(camera_file = video.filename, local_file = "Test.mp4")

if __name__ == "__main__":
    asyncio.run(main())