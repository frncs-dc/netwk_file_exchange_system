import socket
import threading
import os
from datetime import datetime

def receive_file(client_socket, filename,save_directory):
    try:
        full_path = os.path.join(save_directory, filename)
        f = open(full_path, "wb")
        if f:
            data = client_socket.recv(819200)
            f.write(data)
            f.close()
        else:
            print("Error")
    except Exception as e:
        print(f"Error receiving file {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "localhost"
    port = "12345"
    server.bind((ip, int(port)))
    server.listen(5)
    print("Server listening on port " + port)

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
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break

            elif command.startswith('/store'):
                _, filename = command.split()
                save_directory = "Server Directory"
                receive_file(client_socket, filename, save_directory)

            elif command == '/dir':
                directory = "Server Directory"
                isExist = os.path.exists(directory)

                if isExist:
                    files = os.listdir(directory)
                    client_socket.send((directory + ": \n" + convertToString(files)).encode())
                else:
                    os.mkdir(directory)
                    print("Directory '%s' created" % directory)

            elif command == '/?':
                client_socket.send(convertToString(getCommandList()).encode())

            elif command == '/leave':
                client_socket.send("Connection closed. Thank you!".encode())
                client_socket.close()
                print(f"Client {addr} disconnected.")
                break

            else:
                client_socket.send("Error: Rawr Invalid command or handler not registered.".encode())

    except Exception as e:
        client_socket.send(f"Error: {e}".encode())

if __name__ == "__main__":
    start_server()
