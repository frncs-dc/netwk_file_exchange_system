import socket
import threading
import os
from datetime import datetime
import ipaddress
import time

clients = []  # Dictionary to store client handlers
nicknames = []
      # Dictionary to store client handlers

def receive_file(client_socket, filename, save_directory):

    client_directory = getUserName(client_socket)

    if client_directory:
        client_socket.send("Storing File to Server".encode())
        path = os.path.join(client_directory, filename)
        if(os.path.exists(path)):
            time.sleep(0.01)
            file_path = client_directory + " " + filename
            client_socket.send(file_path.encode())

            file_size = os.path.getsize(path) + 1
            data = client_socket.recv(file_size)

            full_path = os.path.join(save_directory, filename)
            f = open(full_path, "wb")
            print(full_path)
            if f:
                f.write(data)
                f.close()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                broadcast_message = f"{client_directory} <{timestamp}>: Uploaded {filename}"
                # client_socket.send(broadcast_message.encode())
                for client in clients:
                    try:
                        print(broadcast_message)
                        time.sleep(0.05)
                        client.send(broadcast_message.encode())
                    except Exception as e:
                        print(f"Error broadcasting to {client}: {e}.")
            else:
                print("Error")
        else:
            client_socket.send("Error: File not found.".encode())
    else:
        client_socket.send("Error: User not registered!".encode())

def fetchFile(client_socket, filename):
    if getUserName(client_socket):
        if (os.path.exists('Server Directory/' + filename )):
            client_socket.send("Sending File to Client".encode())
            user_directory = getUserName(client_socket)
            time.sleep(0.01)
            client_socket.send(user_directory.encode())
            time.sleep(0.01)
            client_socket.send(filename.encode())
            with open('Server Directory/' + filename, 'rb') as f: 
                data = f.read()
                print(data)
                time.sleep(0.05)                              
                client_socket.sendall(data)
        else:
            client_socket.send("Error: File not found in the server.".encode())
    else:
        client_socket.send("Error: User not registered!".encode())
        
        
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input("IP: ")
    port = input("Port: ")
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

def convertToSentence(files):

    dir_list = ''

    for x in files:
        dir_list += x + ' '
    
    return dir_list

def getUserName(client_socket):
    try:
        index = clients.index(client_socket)
        username = nicknames[index]

        return username
    except:
        return False

def findClientSocket(username):
    try:
        index = nicknames.index(username)
        socket = clients[index]

        return socket
    except:
        return False

def handle_client(client_socket, addr):
    handler = None
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break  
            
            elif command.startswith('/register'):
                curr_user = None
                try:
                    curr_user = command.split()[1]
                except:
                    client_socket.send("Error: Command parameters do not match or is not allowed.".encode())
                
                if(curr_user):
                    if os.path.exists(curr_user):
                        client_socket.send("Error: Registration failed. Handle or alias already exists.".encode())
                    else:
                        os.mkdir(curr_user)
                        # client_socket.send(f"Welcome {curr_user}".encode())
                        welcome_message = f"Welcome {curr_user}"
                        clients.append(client_socket)
                        nicknames.append(curr_user)
                        for client in clients:
                            try:
                                print(welcome_message)
                                client.send(welcome_message.encode())
                            except Exception as e:
                                print(f"Error broadcasting to {client}: {e}")

            elif command.startswith('/store'):
                if getUserName(client_socket):
                    try:
                        _, filename = command.split()
                        save_directory = "Server Directory"
                        receive_file(client_socket, filename, save_directory)
                    except:
                        client_socket.send("Error: Command parameters do not match or is not allowed.".encode())
                else:
                    client_socket.send("User not registered".encode())

            elif command.startswith('/get'):
                if getUserName(client_socket):
                    _, filename = command.split()
                    fetchFile(client_socket, filename)
                
                else:
                    client_socket.send("User not registered".encode())
        
            elif command == '/dir':
                if getUserName(client_socket):
                    directory = "Server Directory"
                    isExist = os.path.exists(directory)

                    if(isExist):
                        files = os.listdir(directory)
                        client_socket.send((directory + ": \n" + convertToString(files)).encode())
                    else:
                        os.mkdir(directory) 
                        print("Directory '%s' created" %directory)
                else:
                    client_socket.send("User not registered".encode())
            
            elif command.startswith('/sendToAll'):
                if getUserName(client_socket):
                    messageList = command.split()
                    del messageList[0]
                    message = convertToSentence(messageList)
                    messageToSend = getUserName(client_socket) + ": " + message
                    for client in clients:
                        if client_socket != client:
                            try:
                                client.send(messageToSend.encode())
                            except Exception as e:
                                print(f"Error broadcasting to {client}: {e}")
                        else:
                            client_socket.send("Message sent to all".encode())
                else:
                    client_socket.send("User not registered".encode())
            
            elif command.startswith('/send'):
                if getUserName(client_socket):
                    messageList = command.split()
                    user = messageList[1]
                    del messageList[0]
                    del messageList[0]
                    message = convertToSentence(messageList)
                    messageToSend = getUserName(client_socket) + ": " + message
                    receiver = findClientSocket(user)
                    try:
                        client_socket.send(f"Message sent to {user}".encode())
                        receiver.send(messageToSend.encode())
                    except Exception as e:
                        client_socket.send("User doesn't exist!".encode())
            
                else:
                    client_socket.send("User not registered".encode())

            elif command == '/leave':
                if getUserName(client_socket):
                    curr_user = getUserName(client_socket)
                    for client in clients:
                        if client_socket != client:
                            try:
                                goodbye = f"{curr_user} left the server"
                                print(goodbye)
                                client.send(goodbye.encode())
                            except Exception as e:
                                print(f"Error broadcasting to {client}: {e}")
                        else:
                            client_socket.send("Connection closed. Thank you!".encode())

                    nicknames.remove(curr_user)
                    clients.remove(client_socket)
                    
                    client_socket.close()
                    # break
                else:
                    client_socket.send("Connection closed. Thank you!".encode())
                    if client_socket.recv(4096).decode() == "Goodbye!":
                        client_socket.close()
                        # break

            else:
                 client_socket.send("Error: Command not found.".encode())

    except Exception as e:
        # client_socket.send(f"Error: {e}".encode())
        print(f"Error: {e}")

        
if __name__ == "__main__":
    start_server()