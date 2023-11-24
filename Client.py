import socket
import tkinter as tk
import os
from datetime import datetime
import threading

def getCommandText(textboxCommand):
    command = textboxCommand.get(1.0, 'end-1c')
    useCommand(command)

def receiveFileFromServer(command):
    global curr_user
    global s

    _, filename = command.split()

    try:
        full_path = os.path.join(curr_user, filename)
        with open(full_path, "wb") as f:
            data = s.recv(819200)
            print(data)
            f.write(data)
        print("File received from Server: " + filename)
    except Exception as e:
        print(f"Error receiving file {e}")

def useCommand(command):
    global curr_user
    global s

    if command.startswith('/join'):
        details = command.split()
        server_ip = details[1]
        server_port = int(details[2])
        joinServer(server_ip, server_port)

    elif command == '/dir':
        sendToServer(command)

    elif command == '/?':
        sendToServer(command)

    elif command == '/leave':
        try:
            sendToServer(command)
            s.close()
        except Exception as e:
            print('Error: Disconnection failed. Please connect to the server first')

    elif command.startswith('/store'):
        _, filename = command.split()

        if os.path.exists(curr_user + '/' + filename):
            sendToServer(command)
            with open(curr_user + '/' + filename, 'rb') as f:
                data = f.read()
                s.sendall(data)
            
            broadcast_message = f"User {curr_user} stored file: {filename}"
            s.send(broadcast_message.encode())

            response = s.recv(4096)
            print(f"{curr_user}{response.decode()}")
        else:
            print("Error: File not found.")

    elif command.startswith('/get'):
        sendToServer(command)

    elif command.startswith('/register'):
        try:
            sendToServer(command)
        except Exception as e:
            print(f"Error: {e}")

def sendToServer(command):
    global s
    global curr_user

    s.send(command.encode())
    if command.startswith('/get'):
        receiveFileFromServer(command)
    else:
        response = s.recv(4096)
        print(response.decode())

        if response.decode().startswith('Welcome'):
            curr_user = command.split()[1]

def joinServer(server_ip, server_port):
    global s
    global curr_user
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port))
        print("Connected to the File Exchange Server is successful!")
    except Exception as e:
        print(f"Error: Connection to the Server has failed! Please check IP Address and Port Number. {e}")

def main():
    ROOT = tk.Tk()
    ROOT.geometry("500x500")
    ROOT.title("Python File Sharing")

    labelCommand = tk.Label(ROOT, text="Input Command:", font=('Helvetica', 18))
    labelCommand.pack(padx=10, pady=10)

    textboxCommand = tk.Text(ROOT, height=1, font=('Helvetica', 18))
    textboxCommand.pack()

    buttonCommand = tk.Button(ROOT, text="Enter", font=('Helvetica', 18),
                              command=lambda: threading.Thread(target=getCommandText, args=(textboxCommand,)).start())
    buttonCommand.pack(padx=10, pady=10)

    labelERROR = tk.Label(ROOT, text="Error:", font=('Helvetica', 14))
    labelERROR.pack()

    ROOT.mainloop()

if __name__ == "__main__":
    main()
