import smbus2
import time

# Get I2C bus
bus = smbus2.SMBus(1)

altitudeSensorAddress = 0x60
controlRegisterAddress = 0x26
altitudeControlRegisterAddress = 0x2d
altimeterMode = 0xB9
dataConfigurationRegister = 0x13
dataReadyEvent = 0x07

#currentElevation = 19191


numMinutesToRun = 1.5
startTime = time.time()
endTime = 1.0 * startTime + 60 * numMinutesToRun

#bus.write_byte_data(altitudeSensorAddress, altitudeControlRegisterAddress, currentElevation)

while time.time() < endTime:
    f = open("sensingData.txt", "a")
    bus.write_byte_data(altitudeSensorAddress, controlRegisterAddress, altimeterMode)
    bus.write_byte_data(altitudeSensorAddress, dataConfigurationRegister, dataReadyEvent)
    bus.write_byte_data(altitudeSensorAddress, controlRegisterAddress, altimeterMode)

    time.sleep(1) # wait 1 second for the data to be written back

    numberBytes = 6
    readDataBackRegister = 0x00
    # status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
    data = bus.read_i2c_block_data(altitudeSensorAddress, readDataBackRegister, numberBytes)

    # Convert the data to 20-bits
    tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
    altitude = tHeight / 16.0
    cTemp = temp / 16.0
    fTemp = cTemp * 1.8 + 32

    msb = data[1]
    csb = data[2]
    lsb = data[3]

 # Calculate altitude, check for negative sign in altimeter data
    foo = 0
    if (msb > 1):
        foo = ~(msb << 16 | csb << 8 | lsb) + 1 # 2's complement the data
        altitude_git =  (foo >> 8) + ((lsb >> 4)/16.0) # Whole number plus fraction altitude in meters for negative altitude
        altitude_git *= -1
    else:

        foo = ((msb << 8) | csb)
        altitude_git = (foo) + ((lsb >> 4)/16.0)  #Whole number plus fraction altitude in meters
        

    ##TOM!
    #Altitude = (float) ((short) ((OUT_P_MSB_REG << 8) | OUT_P_CSB_REG )) + (float) (OUT_P_LSB_REG  >> 4) * 0.0625
    #Altitude_tom = ((data[1] << 8) | (data[2])) + (data[3] >> 4) * .0625

    barometerMode = 0x39
    bus.write_byte_data(altitudeSensorAddress, controlRegisterAddress, barometerMode)
    time.sleep(1)

    # status, pres MSB1, pres MSB, pres LSB
    data = bus.read_i2c_block_data(altitudeSensorAddress, readDataBackRegister, 4)

    # Convert the data to 20-bits
    pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    pressure = (pres / 4.0) / 1000.0

    #print ("Data1 : %f" %data[1])
    #print ("Data2 : %f" %data[2])
    #print ("Data3 : %f" %data[3])

    #print(bin(data[1]) + bin(data[2]) + bin(data[3]))

    CO2SensorAddress = 0x08
    gasPPMRegisterAddress = 0x20

    data_CO2 = bus.read_i2c_block_data(CO2SensorAddress, gasPPMRegisterAddress, 2)

    CO2_ppm = ((data_CO2[0] & 0x3F)<<8) | data_CO2[1]

    # Output data to screen\
    print ("Time: %.2f" %(time.time() - startTime))
    print ("Pressure : %.2f kPa" %pressure)
    print ("Altitude : %.2f m" %altitude)
    print ("Altitude Git: %.2f m" %altitude_git)
    print ("Temperature in Celsius  : %.2f C" %cTemp)
    print ("Temperature in Fahrenheit  : %.2f F" %fTemp)
    print ("CO2 Data : "+ str(CO2_ppm) + " ppm\n")
    f.write ("Time: %.2f\n" %(time.time() - startTime))
    f.write ("Pressure : %.2f kPa\n" %pressure)
    f.write ("Altitude : %.2f m\n" %altitude)
    f.write ("Temperature in Celsius  : %.2f C\n" %cTemp)
    f.write ("Temperature in Fahrenheit  : %.2f F\n" %fTemp)
    f.write ("CO2 Data : "+ str(CO2_ppm) + " ppm\n\n")
    time.sleep(1)

    f.close()
