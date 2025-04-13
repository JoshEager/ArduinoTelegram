import serial
import time 


arduinoData = serial.Serial("COM4", 9600)
time.sleep(1) # Wait for the serial to be setup

while True: 
    dataPacket = arduinoData.readline()
    print(dataPacket)
    stringValue = str(dataPacket, "UTF-8")
    stringValue = stringValue.strip("\r\n")
    print(stringValue)

    