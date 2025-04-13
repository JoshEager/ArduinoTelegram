"""

This is a program that is used as a relay for telegraph communication. 
This program needs to:
    - Accept and handle clients
        -> Read serial from clients
        -> Forward the serial read from one client to all other clients

"""

import socket
import threading 


LOCAL_HOST = "0.0.0.0"
LOCAL_PORT = 25555

clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, client_addr): 
    print(f"New connection from {client_addr}")
    with clients_lock:
        clients.append(client_socket)
    
    try: 
        while True:
            bit = client_socket.recv(1)
            print(f"Recieved a {bit.decode()} from {client_addr}")
            if not bit:
                break

            with clients_lock:
                for other_client in clients:
                    if other_client != client_socket:
                        try:
                            other_client.send(bit)
                        except: # Broken client
                            clients.remove(other_client)
                            print("Removed disconnected client")

    except Exception as e:
        print(f"Error with {client_addr}: {e}") 

    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()
        print(f"Disconnected {client_addr}")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LOCAL_HOST, LOCAL_PORT))
    server_socket.listen(5)
    print(f"Server listening on {LOCAL_HOST}:{LOCAL_PORT:d}")

    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
            thread.start()
    
    except Exception as e:
        print(f"Shutting down: {e}")
    
    finally: 
        for client_socket in clients:
            client_socket.close()
        server_socket.close()
        

if __name__ == "__main__":
    main()
