import tkinter as tk
import os

def sendCommand():
    command = textboxCommand.get(1.0,'end-1c')
    print(command)


ROOT = tk.Tk()
ROOT.geometry("500x500")
ROOT.title("Python File Sharing")

labelCommand = tk.Label(ROOT, text="Input Command:", font=('Helvetica', 18))
labelCommand.pack(padx=10, pady=10)

# Inputs the Command Here
textboxCommand = tk.Text(ROOT, height=1, font=('Helvetica', 18))
textboxCommand.pack()

# Clicks this to execute the command
buttonCommand = tk.Button(ROOT, text="Enter", font=('Helvetica', 18), command=sendCommand)
buttonCommand.pack(padx=10, pady=10)


# Displays the error
labelERROR = tk.Label(ROOT, text="Error:", font=('Helvetica', 14))
labelERROR.pack()

ROOT.mainloop()

