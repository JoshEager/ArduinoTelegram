
"""
This is a program that reads serial data from an arduino telegraph and sends it over the internet
to a server. For the sake of sounding correct, all communications are buffered. For example,
if the user inputs a series of 1s, the program will wait until that series is finished before
sending it. If it did not do this, there would be slight delay between each bit, causing an
annoying ticking on all transmissions. 

Behaviors: 
    - When recieving a 1, put it in a buffer and wait until a zero is recieved before sending
        -> This will buffer each dit or dah
    - When actually sending a dit or a dah, just send the number 1s that were read. 
        -> Since 1 is the only data that really ever needs to be sent, it makes sense to
            send it this way to minimize the data being sent
    - One thread should manage sending data, while another should manage incoming data
        -> This ensures that sending is actually possible. To recieve something, you have to
            wait, which is a blocking activity; you would never send if you wait to recieve

"""

from config import ARDUINO_REFRESH_DELAY, TRANSMISSION_BYTES, SERIAL_PORT, BAUDRATE, REMOTE_HOST, REMOTE_PORT
import serial 
import socket 
import threading
import time

def sendTelegram(serialInterface: serial.Serial, client_socket: socket.socket): 
    """ Function to run in its own thread that reads any dits or dahs from the arduino and sends them"""
    outBoundBuffer = []
    while True: 
        # Read a bit from the ardino
        currentBit = serialInterface.readline().decode("utf-8").strip("\r\n")

        # If the bit is a 1, then add it to the outBoundBuffer.
        # If it is a zero, then flush the buffer (if it exists)
        if currentBit == '1':
            outBoundBuffer.append(currentBit)
        else:
            if len(outBoundBuffer) > 0:
                sendDitOrDah(outBoundBuffer, client_socket)
                outBoundBuffer = []
            else: pass 

def sendDitOrDah(ditOrDah: list, client_socket: socket.socket):
    """ Function that sends the duration of either a dit or a dah """
    # Find the number of 1s in the ditOrDah string (it will only ever contain 1s)
    # and then put that in TRANSMISSION_BYTES bytes and send it
    ditOrDahDuration = len(ditOrDah).to_bytes(TRANSMISSION_BYTES, byteorder="big", signed=False)
    client_socket.send(ditOrDahDuration)
    print(f"Sent a {(ARDUINO_REFRESH_DELAY * len(ditOrDah)) / 1000} second {"dit" if len(ditOrDah) * ARDUINO_REFRESH_DELAY / 1000 < .2 else "dah"}")

def recieveTelegram(serialInterface: serial.Serial, client_socket: socket.socket):
    """ Function that should run in its own thread and recieves dits or dahs from the internet """
    while True:
        ditOrDahDuration = int.from_bytes(client_socket.recv(TRANSMISSION_BYTES), byteorder="big", signed=False)
        ditOrDah = "1" * ditOrDahDuration
        for bit in ditOrDah:
            serialInterface.write(bit.encode("utf-8"))
        print(f"Recieved a {(ARDUINO_REFRESH_DELAY * len(ditOrDah)) / 1000} second {"dit" if len(ditOrDah) * ARDUINO_REFRESH_DELAY / 1000 < .2 else "dah"}")

def main():
    serialInterface = serial.Serial(SERIAL_PORT, BAUDRATE)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(.5) # Make sure serial and socket are properly setup
    client_socket.connect((REMOTE_HOST, REMOTE_PORT))
    print(f"Connected to {REMOTE_HOST} on port {REMOTE_PORT}")

    sendThread = threading.Thread(target=sendTelegram, args=(serialInterface, client_socket))
    recieveThread = threading.Thread(target=recieveTelegram, args=(serialInterface, client_socket))
    sendThread.start()
    recieveThread.start()

if __name__ == "__main__":
    main()
