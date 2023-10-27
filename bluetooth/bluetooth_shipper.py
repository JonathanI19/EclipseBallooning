import logging
import asyncio
import platform
import ast

from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover

MOVE_CMD_UUID = '13012F03-F8C3-4F4A-A8F4-15CD926DA146'

stop_code = bytearray([0x00])
ccw_code = bytearray([0x01])
cw_code = bytearray([0x02])

async def popMovementQueue(client):
    val = input('Enter movement command (STOP, CCW, CW) : ')

    if (val == 'stop'):
        await client.write_gatt_char(MOVE_CMD_UUID, stop_code)
    elif (val == 'ccw'):
        await client.write_gatt_char(MOVE_CMD_UUID, ccw_code)
    elif (val == 'cw'):
        await client.write_gatt_char(MOVE_CMD_UUID, cw_code)
    else:
        await client.write_gatt_char(MOVE_CMD_UUID, stop_code)

async def run():
    
    print('ProtoStax Arduino Nano BLE LED Peripheral Central Service')
    print('Looking for Arduino Nano 33 BLE Sense Peripheral Device...')

    found = False
    devices = await BleakScanner.discover()
    for d in devices:       
        if 'Arduino Nano 33 BLE Sense' in d.name:
            print('Found Arduino Nano 33 BLE Sense Peripheral')
            found = True
            async with BleakClient(d.address) as client:
                while True:
                    await popMovementQueue(client)

    if not found:
        print('Could not find Arduino Nano 33 BLE Sense Peripheral')

                    
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')