import smbus2
import time

# Get I2C bus
bus = smbus2.SMBus(1)

altitudeSensorAddress = 0x60
controlRegisterAddress = 0x26
altimeterMode = 0xB9
dataConfigurationRegister = 0x13
dataReadyEvent = 0x07
readDataBackRegister = 0x00
barometerMode = 0x39

numMinutesToRun = 300
startTime = time.time()
endTime = 1.0 * startTime + 60 * numMinutesToRun

while time.time() < endTime:
    f = open("sensingData.txt", "a")
    bus.write_byte_data(altitudeSensorAddress, controlRegisterAddress, altimeterMode)
    bus.write_byte_data(altitudeSensorAddress, dataConfigurationRegister, dataReadyEvent)
    bus.write_byte_data(altitudeSensorAddress, controlRegisterAddress, altimeterMode)

    time.sleep(1) # wait 1 second for the data to be written back

    numberBytes = 6
    # status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
    data = bus.read_i2c_block_data(altitudeSensorAddress, readDataBackRegister, numberBytes)

    # Convert the data to 20-bits
    tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
    altitude = tHeight / 16.0
    cTemp = temp / 16.0
    fTemp = cTemp * 1.8 + 32

    bus.write_byte_data(altitudeSensorAddress, controlRegisterAddress, barometerMode)
    time.sleep(1)

    # status, pres MSB1, pres MSB, pres LSB
    data = bus.read_i2c_block_data(altitudeSensorAddress, readDataBackRegister, 4)

    # Convert the data to 20-bits
    pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    pressure = (pres / 4.0) / 1000.0

    CO2SensorAddress = 0x08
    gasPPMRegisterAddress = 0x20

    data = bus.read_i2c_block_data(CO2SensorAddress, gasPPMRegisterAddress, 2)

    CO2_ppm = ((data[0] & 0x3F)<<8) | data[1]

    # Output data to screen\
    print ("Time: %.2f" %time.time())
    print ("Pressure : %.2f kPa" %pressure)
    print ("Altitude : %.2f m" %altitude)
    print ("Temperature in Celsius  : %.2f C" %cTemp)
    print ("Temperature in Fahrenheit  : %.2f F" %fTemp)
    print ("CO2 Data : "+ str(CO2_ppm) + " ppm\n")

    f.write("%.2f," %time.time())
    f.write("%.2f," %pressure)
    f.write("%.2f," %altitude)
    f.write("%.2f," %cTemp)
    f.write("%.2f," %fTemp)
    f.write(str(CO2_ppm) + "\n")
    '''
    Format of data...
    Time:
    Pressure: kpa
    Altitude: m
    Temperature in Celcius:
    Temperature in Farenheit:
    CO2 PPM: 
    '''

    f.close()
