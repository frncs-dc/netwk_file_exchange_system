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

def receiveFileFromServer(user_directory, filename, data, outputString):

    global curr_user
    global s

    full_path = os.path.join(user_directory, filename)
    f = open(full_path, "wb")
    f.write(data)
    f.close()
    print("File received from Server: " + filename)
    outputString.set("File received from Server: " + filename)

def storeFileToServer(client_directory, filename, outputString):

    with open(client_directory + '/' + filename, 'rb') as f:       
        data = f.read()                                     
        s.sendall(data)                          

    response = s.recv(4096)
    print(f"{client_directory}{response.decode()}")
    outputString.set(f"{client_directory}{response.decode()}")

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
            sendToServer(command)
        except:
            print("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            outputString.set("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
    
    elif command == '/leave':
        try:
            sendToServer(command)
        except Exception as e:
            print('Error: Disconnection failed. Please connect to the server first')
    
    elif command == '/dir':
        sendToServer(command)

    elif command == '/?':
        sendToServer(command)

    elif command.startswith('/store'):
        sendToServer(command)                  
        
    elif command.startswith('/get'):
        sendToServer(command)        
    
    else: 
        outputString.set("Error: Command not found.")

def sendToServer(command):
    global s
    global curr_user

    s.send(command.encode())

def receive(outputString):
    global curr_user
    global exit_flag
    global s

    while not exit_flag.is_set():
        try:
            output = s.recv(4096)

            if output.decode().startswith('Welcome'):
                outputString.set(output.decode())
                curr_user = output.decode().split()[1]
            elif output.decode().startswith('Sending File to Client'):
                user_directory = s.recv(4096).decode()
                filename = s.recv(4096).decode()
                data = s.recv(819200)
                receiveFileFromServer(user_directory, filename, data, outputString)
            elif output.decode().startswith('Storing File to Server'):
                ifFileExists = s.recv(4096).decode()
                if not ifFileExists.startswith("Error"):
                    client_directory = s.recv(4096).decode()
                    filename = s.recv(4096).decode()
                    storeFileToServer(client_directory, filename, outputString)
            elif output.decode().startswith('Connection closed'):
                s.close()
            else:
                # others
                print(output.decode())
                outputString.set(output.decode())
        except Exception as e:
            print(f"Error in Threading {e}")
            outputString.set(f"Error in Threading {e}")  
            break

def startThreading(outputString):
    receive_thread = threading.Thread(target=receive, args=(outputString,))
    receive_thread.start()

def joinServer(server_ip, server_port, outputString):
    global s
    global curr_user
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port));
        outputString.set("Connection to the File Exchange Server is successful!")
        print("Connection to the File Exchange Server is successful!")
        startThreading(outputString)
    except:
        outputString.set("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
        print("Error: Connection to the Server has failed! Please check IP Address and Port Number.") 

def main():
    global s
    global curr_user
    global exit_flag

    exit_flag = threading.Event()
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

    ROOT.mainloop()

if __name__ == "__main__":
    main()
