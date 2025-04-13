"""

This is a program that is intended to help an arduino in becoming a telegram. 
The program reads a bit every 20ms from the arduino, and it also writes a bit
every 20ms to the arduino. The bit that it writes comes from the internet, 
which is used in order to connect the devices to one another. This is 
necessary because an uno r3 is not capable of connecting to the internet on 
its own, so it needs a 'helper device'. 

    If the program get a zero from the internet, then the buzzer should not go
off on the arduino. Conversely, if the program reads a one from the internet,
then the buzzer will go off on the arduino.
    If the program reads a zero from the arduino, then it will send the 
internet a zero. Conversely if the program reads a 1 from the arduino, it will
send the internet a 1.  

"""


import serial
import time 
import socket


SERIAL_PORT = "COM4"
BAUD_RATE = 115200
REMOTE_HOST = "127.0.0.1"
REMOTE_PORT = 25555

serialInterface = serial.Serial(SERIAL_PORT, BAUD_RATE)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(1) # Ensure serial and sockets are properly set up


def main():
    client_socket.connect((REMOTE_HOST, REMOTE_PORT))
    print(f"Connected to {REMOTE_HOST} on port {REMOTE_PORT:d}")

    try: 
        while True:
            try:
                arduinoBit = int(serialInterface.readline())
            except Exception as e:
                print(f"error reading arduino bit: {e}")
                arduinoBit = 0

            if arduinoBit == 0 or arduinoBit == 1: 
                client_socket.send(str(arduinoBit).encode("utf-8"))
                print(f"Send: {arduinoBit}")
            try:
                internetBit = int(client_socket.recv(1))
            except: 
                internetBit = 0
            if internetBit == 0 or internetBit == 1:
                serialInterface.write(str(internetBit).encode("utf-8"))
                print(f"Recieved: {internetBit}")

    except Exception as e:
        print(f"Error: {e}")

    finally: 
        client_socket.close()


if __name__ == "__main__":
    main()
