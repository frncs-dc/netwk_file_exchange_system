import socket
import threading
import os
from datetime import datetime
import ipaddress

clients = {}  # Dictionary to store client handlers
lock = threading.Lock()
def receive_file(client_socket, filename,save_directory):
    try:
        full_path = os.path.join(save_directory, filename)
        f = open(full_path, "wb")
        print(full_path)
        if f:
            data = client_socket.recv(819200)
            f.write(data)
            f.close()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_socket.send(f"{timestamp}: File {filename} stored successfully.".encode())
        else:
            print("Error")
    except Exception as e:
        print(f"Error receiving file {e}")

def fetchFile(client_socket, filename):
    if (os.path.exists('Server Directory/' + filename )):
        client_socket.send("True".encode())
        with open('Server Directory/' + filename, 'rb') as f: 
            data = f.read()
            print(data)                              
            client_socket.sendall(data)
    else:
        client_socket.send("Error: File not found in the server.")
        


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip = input()
    # port = input()
    ip = "localhost"
    port = "12345"
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

def broadcast(message):
    with lock:
        for handler, client_socket in clients.items():
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting to {handler}: {e}")              


def handle_client(client_socket, addr):
    handler = None
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break  
            
            elif command.startswith('/register'):
                curr_user = command.split()[1]
                if os.path.exists(curr_user):
                    client_socket.send("Error: Registration failed. Handle or alias already exists.".encode())
                else:
                    os.mkdir(curr_user)
                    client_socket.send(f"Welcome {curr_user}".encode())

            elif command.startswith('/store'):
                _, filename = command.split()
                save_directory = "Server Directory"
                receive_file(client_socket, filename, save_directory)
                
            elif command.startswith('/get'):
                _, filename = command.split()
                fetchFile(client_socket, filename)
        
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
                client_socket.send("Error: Invalid command or handler not registered.".encode())

    except Exception as e:
        client_socket.send(f"Error: {e}".encode())

        
if __name__ == "__main__":
    start_server()