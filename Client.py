import socket
import tkinter as tk
import os
from datetime import datetime
import threading
import time

def joinServer(server_ip, server_port, outputString, serverStatus):
    global s
    global curr_user
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port));
        outputString.set("Connection to the File Exchange Server is successful!")
        print("Connection to the File Exchange Server is successful!")
        startThreading(outputString, serverStatus)
    except:
        outputString.set("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
        print("Error: Connection to the Server has failed! Please check IP Address and Port Number.") 

def getCommandList():
    cmd_list = [
                "/? - Request command help to output all Input Syntax commands for references",
                "/join <server_ip_add> <port> - Connect to the server application",
                "/leave - Disconnect to the server application",
                "/register <handle> - Register a unique handle or alias",
                "/store <filename> - Send file to server",
                "/dir - Request directory file list from a server",
                "/get <filename> - Fetch a file from a server",
                "/sendToAll <message> - send a message to all registered and connected users",
                "/send <user> <message> - send a message to one specific user" 
    ]

    return cmd_list

def convertToString(files):

    dir_list = ''

    for x in files:
        dir_list += x + '\n'
    
    return dir_list

def getCommandText(textboxCommand, outputString, serverStatus):
    # gets the command from the text inputted
    command = textboxCommand.get(1.0,'end-1c')

    # function to see which command would be used
    useCommand(command, outputString, serverStatus)

def receiveFileFromServer(user_directory, filename, data, outputString):

    try:
        full_path = os.path.join(user_directory, filename)
        f = open(full_path, "wb")
        f.write(data)
        f.close()
        print("File received from Server: " + filename)
        outputString.set("File received from Server: " + filename)
    except Exception as e:
        print(f"Error: {e}")
    
def storeFileToServer(client_directory, filename, outputString):

    global s
    
    try:
        print("User:" + client_directory)
        print("Filename:" + filename)
        full_path = os.path.join(client_directory, filename)
        f = open(full_path, 'rb')       
        data = f.read()
        f.close()
        time.sleep(0.5)                                     
        s.sendall(data)                          
    except Exception as e:
        print(f"Error: {e}")

def useCommand(command, outputString, serverStatus):
    global curr_user
    global s

    if command.startswith('/join'):
        try:
            details = command.split()
            server_ip = details[1]
            server_port = int(details[2])
            joinServer(server_ip, server_port, outputString, serverStatus)
        except:
            outputString.set("Error: Command parameters do not match or is not allowed.")
    
    elif command == '/?':
        outputString.set(convertToString(getCommandList()))

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
            outputString.set('Error: Disconnection failed. Please connect to the server first')
    
    elif command == '/dir':
        try:
            sendToServer(command)
        except Exception as e:
            print("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            outputString.set("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")

    elif command.startswith('/store'):
        try:
            sendToServer(command)              
        except:
            print("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            outputString.set("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
          
    elif command.startswith('/get'):
        try:
            sendToServer(command)
        except:
            print("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            outputString.set("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            
    elif command.startswith('/sendToAll'):
        try:
            sendToServer(command)
        except:
            print("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            outputString.set("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
    
    elif command.startswith('/send'):
        try:
            sendToServer(command)
        except:
            print("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            outputString.set("Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination")
            
    else: 
        outputString.set("Error: Command not found.")

def sendToServer(command):
    global s
    global curr_user

    s.send(command.encode())

def receive(outputString, serverStatus):
    global curr_user
    global exit_flag
    global s

    while not exit_flag.is_set():
        try:
            time.sleep(0.02)
            output = s.recv(4096).decode()  

            if output.startswith('Welcome'):
                serverStatus.set(output)
                curr_user = output.split()[1]
            elif output.startswith('Sending File to Client'):
                user_directory = s.recv(4096).decode()
                filename = s.recv(4096).decode()
                data = s.recv(819200)
                receiveFileFromServer(user_directory, filename, data, outputString)

            elif output.startswith('Storing File to Server'):
                time.sleep(0.02)
                response = s.recv(1024).decode()
                if not response.startswith("Error"):
                    time.sleep(0.02)
                    print("Response: " + response)
                    client_directory, filename = response.split()
                    storeFileToServer(client_directory, filename, outputString)
                else:
                    print(response)
                    outputString.set(response)
            elif output.startswith('Connection closed'):
                s.send("Goodbye!".encode())
                s.close()
                serverStatus.set("Connection closed. Thank you!")
                outputString.set("")
                break
            else:
                # others
                print(output)
                outputString.set(output)
        except Exception as e:
            print(f"Error in Threading {e}")
            outputString.set(f"Error in Threading {e}")  
            break

def startThreading(outputString, serverStatus):
    receive_thread = threading.Thread(target=receive, args=(outputString, serverStatus))
    receive_thread.start()



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
    serverStatus= tk.StringVar()


    labelCommand = tk.Label(ROOT, text="Input Command:", font=('Helvetica', 18))
    labelCommand.pack(padx=10, pady=10)

    # Inputs the Command Here
    textboxCommand = tk.Text(ROOT, height=1, font=('Helvetica', 18))
    textboxCommand.pack(padx=30, pady=10)

    # Clicks this to execute the command
    buttonCommand = tk.Button(ROOT, text="Enter", font=('Helvetica', 18), 
                              command=lambda:getCommandText(textboxCommand, outputString, serverStatus))
    buttonCommand.pack(padx=10, pady=10)

    # Displays the output
    labelOutputTitle = tk.Label(ROOT, text="Output Area:", font=('Helvetica', 14))
    labelOutputTitle.pack()
    labelOutput = tk.Label(ROOT, textvariable=outputString,
                           font=('Helvetica', 14),
                           wraplength=450,
                           justify="center")
    labelOutput.pack(padx=10)

    # Displays the Server Status
    labelOutputTitle = tk.Label(ROOT, text="Server Status:", font=('Helvetica', 14))
    labelOutputTitle.pack()
    labelOutput = tk.Label(ROOT, textvariable=serverStatus,
                           font=('Helvetica', 14),
                           wraplength=450,
                           justify="center")
    labelOutput.pack(padx=10)

    ROOT.mainloop()

if __name__ == "__main__":
    main()
