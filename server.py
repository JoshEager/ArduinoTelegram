"""
This is a program that is simply responsible for forwarding transmissions from one client
to another. 

Behaviors: 
    - Recieves a duration from a client and forwards that to all the other clients
        -> This "duration" is just a 16 byte, unsigned, and big endian integer that is directly
            proportional to the amount of time that a dit or dah lasts. 
                - None of this is important though because the server literally does not care.

"""
from config import REMOTE_PORT, TRANSMISSION_BYTES
import socket 
import threading
import typing 


clients: typing.List[socket.socket] = []
clients_lock = threading.Lock()

def forwardTelegrams(client_socket: socket.socket, client_address):
    """ 
        Function that should run in its own thread and will forward ditOrDah durations 
        from one client to all the others. 
    """
    print(f"New connection from {client_address}")
    with clients_lock:
        clients.append(client_socket)
    
    try:
        while True:
            ditOrDahDuration = client_socket.recv(TRANSMISSION_BYTES)
            if not ditOrDahDuration:
                break
            
            with clients_lock:
                for other_client in clients:
                    if other_client != client_socket:
                        try:
                            other_client.send(ditOrDahDuration)
                        except: # Broken client
                            clients.remove(other_client)
                            print("Removed disconnected client")
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
            client_socket.close()
            print(f"Disconnected {client_address}")

def main(): 
    """ Main handles initializing connections """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", REMOTE_PORT))
    server_socket.listen(5)
    print(f"Server listening on 0.0.0.0:{REMOTE_PORT}")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=forwardTelegrams, args=(client_socket, client_address))
            thread.start()
    except Exception as e:
        print(f"Shutting down: {e}")
    finally:
        for client_socket in clients:
            client_socket.close()
        server_socket.close()