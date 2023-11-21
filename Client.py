import socket
import tkinter as tk
import os

<<<<<<< Updated upstream
ROOT = tk.Tk()
ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="Test",
                                  prompt="What's your Name?:")
# check it 
print("Hello", USER_INP)

ROOT.geometry("500x500")
ROOT.title("Python File Sharing")
=======
def getCommandText(my_socket, textboxCommand):
    # gets the command from the text inputted
    command = textboxCommand.get(1.0,'end-1c')
>>>>>>> Stashed changes

    # function to see which command would be used
    useCommand(command, my_socket)

def useCommand(command, s):
    if command.startswith('/join'):
        details = command.split()
        server_ip = details[1]
        server_port = int(details[2])
        joinServer(server_ip, server_port, s)
    
    elif command == '/leave':
        sendToServer(s, command)

    elif command.startswith('/store'):
        _, filename = command.split()
        sendToServer(s, command)
        try:
            with open(filename, 'rb') as f:
                data = f.read()
                s.sendall(data)
        except FileNotFoundError:
            print("Error: File not found.")

def sendToServer(s, command):
    s.send(command.encode())
    response = s.recv(4096)
    print(response.decode())

<<<<<<< Updated upstream
ROOT.mainloop()

import socket

def send_command(s, command):
    s.send(command.encode())
    response = s.recv(4096)
    print(response.decode())
    
def main():
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        print("Connected to the File Exchange Server is successful!")

    while True:
            
            command = input("Enter command: ")
            if command == '/leave':
                send_command(s, command)
                print("Connection closed. Thank you!")
                break

            elif command.startswith('/store'):
                _, filename = command.split()
                send_command(s, command)
                try:
                    with open(filename, 'rb') as f:
                        data = f.read()
                        s.sendall(data)
                except FileNotFoundError:
                    print("Error: File not found.")
                    continue
                
            else:
                send_command(s, command)

if __name__ == "__main__":
    main()  
=======
def checkRegistered(user):
    # code here
    isExist = os.path.exists(user)

    return isExist

def joinServer(server_ip, server_port, s):
    try:
        s.connect((server_ip, server_port));
        print("Connected to the File Exchange Server is successful!")
    except:
        print("Error!")

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    ROOT = tk.Tk()
    ROOT.geometry("500x500")
    ROOT.title("Python File Sharing")

    labelCommand = tk.Label(ROOT, text="Input Command:", font=('Helvetica', 18))
    labelCommand.pack(padx=10, pady=10)

    # Inputs the Command Here
    textboxCommand = tk.Text(ROOT, height=1, font=('Helvetica', 18))
    textboxCommand.pack()

    # Clicks this to execute the command
    buttonCommand = tk.Button(ROOT, text="Enter", font=('Helvetica', 18), 
                              command=lambda:getCommandText(my_socket, textboxCommand))
    buttonCommand.pack(padx=10, pady=10)


    # Displays the error
    labelERROR = tk.Label(ROOT, text="Error:", font=('Helvetica', 14))
    labelERROR.pack()

    ROOT.mainloop()

if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
