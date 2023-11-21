import socket
import tkinter as tk
import os

def getCommandText(my_socket, textboxCommand):
    # gets the command from the text inputted
    command = textboxCommand.get(1.0,'end-1c')

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

    elif command.startswith('/register'):
        _, handler = command.split()
        sendToServer(s, command)

def sendToServer(s, command):
    s.send(command.encode())
    response = s.recv(4096)
    print(response.decode())

def checkRegistered(user):
    # code here
    print("Enter Username: ")
    user = input()
    if os.path.exists(user):
        return True
    else:
        return print("Unregistered User")

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
