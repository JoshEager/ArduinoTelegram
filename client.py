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
import threading

SERIAL_PORT = "COM3"
BAUD_RATE = 115200
REMOTE_HOST = "telegram.moddedminecraft.uk"
REMOTE_PORT = 25555

serialInterface = serial.Serial(SERIAL_PORT, BAUD_RATE)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(1) # Ensure serial and sockets are properly set up

def sendIfHIGH():
    try: 
        outBoundBits = []
        while True:
            # Reading the bit from Serial
            try:
                currentBit = int(serialInterface.readline())
            except Exception as e:
                print(f"error reading arduino bit: {e}")
                currentBit = 0
            print(currentBit)
            
            # If the bit is a 1 then add it to outbound bits. 
            # If it is a zero then check to see if there are outbound bits
            # If there are outbound bits, then you need to send them because that's the end of the
            # sentence. You should then also clear the outbound bits. If there are not, do nothing. 
            if currentBit == 1:
                outBoundBits.append(1)
            else: # if currentBit == 0
                if len(outBoundBits) > 0:
                    for outBoundBit in outBoundBits:
                        client_socket.send(str(outBoundBit).encode("utf-8"))
                    print(f"Sent: {str(outBoundBits)}")
                    outBoundBits = []
                else: 
                    pass

    except Exception as e:
        print(f"Error: {e}")

    finally: 
        client_socket.close()

def recvIfHIGH():
    try:
        while True: 
            # Recieve a bit from the server. If there is no message actively being sent this will hang 
            try:
                internetBit = int(client_socket.recv(1))

            except Exception as e: 
                print(f"Error recieving bit: {e}")
                break

            if internetBit == 1:
                serialInterface.write(str(internetBit).encode("utf-8"))
                print(f"Recieved: {internetBit}")

    except Exception as e:
        print(f"Error Recieving: {e}")


def main():
    client_socket.connect((REMOTE_HOST, REMOTE_PORT))
    print(f"Connected to {REMOTE_HOST} on port {REMOTE_PORT:d}")
    sendThread = threading.Thread(target=sendIfHIGH)
    sendThread.start()
    recvThread = threading.Thread(target=recvIfHIGH)
    recvThread.start()
    


if __name__ == "__main__":
    main()
