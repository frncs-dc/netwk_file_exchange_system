# def getError():
#     print("error")

# def request_directory(command):
#     if command != '/dir':
#         getError()
    
#     else:


# request_directory("/dir")
import socket
import threading
import os
from datetime import datetime
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

def convertToString(files):

    dir_list = ''

    for x in files:
        dir_list += x + '\n'
    
    return dir_list

def getCommandList():
    cmd_list = [
                "/? - Request command help to output all Input Syntax commands for references",
                "/join <server_ip_add> <port> - Connect to the server application",
                "/leave - Disconnect to the server application",
                "/register <handle> - Register a unique handle or alias",
                "/store <filename> - Send file to server",
                "/dir - Request directory file list from a server",
                "/get <filename> - Fetch a file from a server" 
    ]

    return cmd_list

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
                if os.path.exists(handler):
                    client_socket.send(f"Error: Registration failed. Handler or alias already exists.".encode())
                else:
                    os.mkdir(handler)
                    client_socket.send(f"Welcome {handler}.".encode())

            elif command.startswith('/store') and os.path.exists(handler):
                _, filename = command.split()
                client_socket.send("Receiving file...".encode())
                receive_file(client_socket, filename)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                client_socket.send(f"{timestamp}: File {filename} stored successfully.".encode())
        
            elif command == '/dir':
                directory = "Server Directory"
                isExist = os.path.exists(directory)

                if(isExist):
                    files = os.listdir(directory)
                    client_socket.send((directory + ": \n" + convertToString(files)).encode())
                else:
                    os.mkdir(directory) 
                    print("Directory '%s' created" %directory)
            
            elif command == '/?':
                client_socket.send(convertToString(getCommandList()).encode())

            elif command == '/leave':
                client_socket.send("Connection closed. Thank you!".encode())
                client_socket.close()
                if handler:
                    del clients[handler]
                print(f"Client {addr} disconnected.")
                break

            else:
                client_socket.send("Error: Rawr Invalid command or handler not registered.".encode())

    except Exception as e:
        client_socket.send(f"Error: {e}".encode())

        
if __name__ == "__main__":
    start_server()