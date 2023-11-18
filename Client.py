import tkinter as tk
from tkinter import simpledialog

ROOT = tk.Tk()
ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="Test",
                                  prompt="What's your Name?:")
# check it 
print("Hello", USER_INP)

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