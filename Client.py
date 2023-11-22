import socket
import tkinter as tk
import os

def getCommandText(textboxCommand):
    # gets the command from the text inputted
    command = textboxCommand.get(1.0,'end-1c')

    # function to see which command would be used
    useCommand(command)

def useCommand(command):
    global curr_user
    global s

    if command.startswith('/join'):
        if(curr_user):
            details = command.split()
            server_ip = details[1]
            server_port = int(details[2])
            joinServer(server_ip, server_port)
        else:
            print("Register user first!")

    elif command == '/dir':
        sendToServer(command)

    elif command == '/?':
        sendToServer(command)

    elif command == '/leave':
        sendToServer(command)
        s.close()

    elif command.startswith('/store'):
        _, filename = command.split()
        sendToServer(command)
        try:
            with open(curr_user + '/' + filename, 'rb') as f:
                data = f.read()
                s.sendall(data)        
        except:   
            print("Error: File not found.")
        response = s.recv(4096)
        print(response.decode())

    elif command.startswith('/register'):
        curr_user = command.split()[1]
        if os.path.exists(curr_user):
            print("User already exists!")
        else:
            os.mkdir(curr_user)

def sendToServer(command):
    global s

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

def joinServer(server_ip, server_port):
    global s
    global curr_user
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port));
        print("Connected to the File Exchange Server is successful!")
        print(curr_user + "has joined the server!")
    except:
        print("Error!")

def main():
    global s
    global curr_user

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
                              command=lambda:getCommandText(textboxCommand))
    buttonCommand.pack(padx=10, pady=10)


    # Displays the error
    labelERROR = tk.Label(ROOT, text="Error:", font=('Helvetica', 14))
    labelERROR.pack()

    ROOT.mainloop()

if __name__ == "__main__":
    main()
