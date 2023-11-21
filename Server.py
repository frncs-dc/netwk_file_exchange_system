<<<<<<< Updated upstream
=======
# def getError():
#     print("error")

# def request_directory(command):
#     if command != '/dir':
#         getError()
    
#     else:
#         directory = "Directory"
#         isExist = os.path.exists(directory)

#         if(isExist):
#             print("Directory exists")
#             files = os.listdir(directory)
#             print(files)
#         else:
#             os.mkdir(directory) 
#             print("Directory '%s' created" %directory)

# request_directory("/dir")
>>>>>>> Stashed changes
import socket
import threading
import os
from datetime import datetime
<<<<<<< Updated upstream

clients = {}  # Dictionary to store client handlers

=======
import ipaddress

clients = {}  # Dictionary to store client handlers

def receive_file(client_socket, filename):
    with open(filename, 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input()
    port = input()
    server.bind((ip, int(port)))
    server.listen(5)
    print("Server listening on port" + port)

    while True:
        client, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()

>>>>>>> Stashed changes
def handle_client(client_socket, addr):
    handler = None
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break
<<<<<<< Updated upstream

=======
            
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======
                client_socket.close()
                if handler:
                    del clients[handler]
                print(f"Client {addr} disconnected.")
>>>>>>> Stashed changes
                break

            else:
                client_socket.send("Error: Invalid command or handler not registered.".encode())

    except Exception as e:
        client_socket.send(f"Error: {e}".encode())

<<<<<<< Updated upstream
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

=======
        
>>>>>>> Stashed changes
if __name__ == "__main__":
    start_server()