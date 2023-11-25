import socket
import tkinter as tk
import os
from datetime import datetime
import threading


def getCommandText(textboxCommand, outputString):
    # gets the command from the text inputted
    command = textboxCommand.get(1.0,'end-1c')

    # function to see which command would be used
    useCommand(command, outputString)

def receiveFileFromServer(command, outputString):

    global curr_user
    global s
       
    response = s.recv(4096)
    print(response.decode())
    if response.decode() == "True":
        data = s.recv(819200)
        _, filename = command.split()
        full_path = os.path.join(curr_user, filename)
        f = open(full_path, "wb")
        f.write(data)
        f.close()
        print("File received from Server: " + filename)
        outputString.set("File received from Server: " + filename)
    else:
        outputString.set(response.decode())
        

def useCommand(command, outputString):
    global curr_user
    global s

    if command.startswith('/join'):
        try:
            details = command.split()
            server_ip = details[1]
            server_port = int(details[2])
            joinServer(server_ip, server_port, outputString)
        except:
            outputString.set("Error: Command parameters do not match or is not allowed.")
    elif command.startswith('/register'):
        try:
            sendToServer(command, outputString)
        except:
            print("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            outputString.set("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
    
    elif command == '/leave':
        try:
            sendToServer(command, outputString)
            s.close()
        
        except Exception as e:
            print('Error: Disconnection failed. Please connect to the server first')

    elif not curr_user:
        outputString.set("Error: Command parameters do not match or is not allowed.")
    
    elif command == '/dir' and curr_user:
        sendToServer(command, outputString)

    elif command == '/?' and curr_user:
        sendToServer(command, outputString)

    elif command.startswith('/store') and curr_user:
        try:
            _, filename = command.split()
        except:
            print("Error: Command parameters do not match or is not allowed.")
            outputString.set("Error: Command parameters do not match or is not allowed.")

        if(os.path.exists(curr_user + '/' + filename )):            # checks if the file is in the dir
            sendToServer(command, outputString)                                   # sends the command to the server process
            with open(curr_user + '/' + filename, 'rb') as f:       # reads the content of the file if it exists
                data = f.read()                                     # assign the content of the file to 'data'
                s.sendall(data)                                     # send 
            response = s.recv(4096)
            print(f"{curr_user}{response.decode()}")
            outputString.set(f"{curr_user}{response.decode()}")
        else:
            outputString.set("Error: File not found.")

        broadcast_message = f"User {curr_user} stored file: {filename}"
        s.send(broadcast_message.encode())
        
    elif command.startswith('/get') and curr_user:
        sendToServer(command, outputString)        
    
    else:
        outputString.set("Error: Command not found.")

def sendToServer(command, outputString):
    global s
    global curr_user

    s.send(command.encode())
    if command.startswith('/get'):
        receiveFileFromServer(command, outputString)
    else:
        response = s.recv(4096)
        print(response.decode())
        outputString.set(response.decode())

        if response.decode().startswith('Welcome'):
            curr_user = command.split()[1]
            

def joinServer(server_ip, server_port, outputString):
    global s
    global curr_user
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port));
        outputString.set("Connection to the File Exchange Server is successful!")
        print("Connection to the File Exchange Server is successful!")

    except:
        outputString.set("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
        print("Error: Connection to the Server has failed! Please check IP Address and Port Number.") 

def main():
    global s
    global curr_user

    curr_user = None

    ROOT = tk.Tk()
    ROOT.geometry("500x500")
    ROOT.title("Python File Sharing")

    outputString = tk.StringVar()

    labelCommand = tk.Label(ROOT, text="Input Command:", font=('Helvetica', 18))
    labelCommand.pack(padx=10, pady=10)

    # Inputs the Command Here
    textboxCommand = tk.Text(ROOT, height=1, font=('Helvetica', 18))
    textboxCommand.pack(padx=30, pady=10)

    # Clicks this to execute the command
    buttonCommand = tk.Button(ROOT, text="Enter", font=('Helvetica', 18), 
                              command=lambda:getCommandText(textboxCommand, outputString))
    buttonCommand.pack(padx=10, pady=10)

    # Displays the output
    labelOutputTitle = tk.Label(ROOT, text="Output Area:", font=('Helvetica', 14))
    labelOutputTitle.pack()
    labelOutput = tk.Label(ROOT, textvariable=outputString,
                           font=('Helvetica', 14),
                           wraplength=450,
                           justify="center")
    labelOutput.pack(padx=10)

    # # Displays the error
    # labelERROR = tk.Label(ROOT, text="Error:", font=('Helvetica', 14))
    # labelERROR.pack()

    ROOT.mainloop()

if __name__ == "__main__":
    main()
