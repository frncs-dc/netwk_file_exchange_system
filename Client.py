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
    ctr_join = 0

    if command.startswith('/join'):
        if(curr_user and ctr_join == 0):
            details = command.split()
            server_ip = details[1]
            server_port = int(details[2])
            joinServer(server_ip, server_port)
            ctr_join +=  1
        elif(ctr_join > 0):
            print("You are already in a server") #added for now
        else:
            print("Register user first!")

    elif command == '/dir':
        sendToServer(command)

    elif command == '/?':
        sendToServer(command)

    elif command == '/leave':
        if(ctr_join == 1):
            sendToServer(command)
            s.close()
        else:
            print("Error: Disconnection failed. Please connect to the server first.")

    elif command.startswith('/store'):
        _, filename = command.split()
        
        if(os.path.exists(curr_user + '/' + filename )):            # checks if the file is in the dir
            sendToServer(command)                                   # sends the command to the server process
            with open(curr_user + '/' + filename, 'rb') as f:       # reads the content of the file if it exists
                data = f.read()                                     # assign the content of the file to 'data'
                s.sendall(data)                                     # send 
            response = s.recv(4096)
            print(curr_user + response.decode())
        else:
            print("Error: File not found.")

    elif command.startswith('/register'):
        curr_user = command.split()[1]
        if os.path.exists(curr_user):
            print("Error: Registration failed. Handle or alias already exists.")
        else:
            os.mkdir(curr_user)
            print(f"Welcome {curr_user}!")
    

def sendToServer(command):
    global s

    s.send(command.encode())
    response = s.recv(4096)
    print(response.decode())

def joinServer(server_ip, server_port):
    global s
    global curr_user
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port));
        print("Connected to the File Exchange Server is successful!")
    except:
        print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")

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
