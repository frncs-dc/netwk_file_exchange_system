import socket
import threading
import os
from datetime import datetime

clients = {}  # Dictionary to store client handlers

def handle_client(client_socket, addr):
    handler = None
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break

            if command.startswith('/register'):
                handler = command.split()[1]
                clients[handler] = client_socket
                client_socket.send(f"Handle registered as {handler}".encode())

            elif command.startswith('/store') and handler:
                _, filename = command.split()
                client_socket.send("Receiving file...".encode())
                receive_file(client_socket, filename)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                client_socket.send(f"{timestamp}: File {filename} stored successfully.".encode())
        
            elif command == '/leave':
                client_socket.send("Connection closed. Thank you!".encode())
                break

            else:
                client_socket.send("Error: Invalid command or handler not registered.".encode())

    except Exception as e:
        client_socket.send(f"Error: {e}".encode())

    finally:
        client_socket.close()
        if handler:
            del clients[handler]
        print(f"Client {addr} disconnected.")


def receive_file(client_socket, filename):
    with open(filename, 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('111.1.1.1', 8675))
    server.listen(5)
    print("Server listening on port 8675")

    while True:
        client, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()