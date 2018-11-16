# TkInter
# Using Python TkInter, create a GUI application that satisfy the following requirements:
# *It uses a grid view.
# *It has at least 2 entry widgets.
# *It has at least 1 button with a callback function.
# *It has a file menu:
#   *open
#   *save
#   *seperator
#   *quit
#   *It has a at least 1 messagebox, and 1 confirmation messagebox.
# Implement this in a seperate.py file.

import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog

LogInWindow = tk.Tk()


# login window
def login():
    global userE
    global passE
    if userE.get() == 'username' and passE.get() == 'password':
        i = tk.Label(LogInWindow, text='Login success').grid(row=6, column=0)
        print("login success")
        welcome()
    else:
        print("invalid login")
        j = tk.Label(LogInWindow, text='Login failed').grid(row=6, column=0)


LogInWindow.title("MCLogin-Login")

userL = tk.Label(LogInWindow, text="username").grid(row=3, column=0)
passL = tk.Label(LogInWindow, text="password").grid(row=4, column=0)

userE = tk.Entry(LogInWindow)
userE.grid(row=3, column=1)
passE = tk.Entry(LogInWindow, show="*")
passE.grid(row=4, column=1)

logInB = tk.Button(LogInWindow, text="LOGIN", command=login).grid(row=5)
closeB = tk.Button(LogInWindow, text='QUIT', command=quit).grid(row=5, column=1, sticky='e')


# after login
def welcome():
    LogInWindow.withdraw()
    top = tk.Toplevel()
    top.title('MCLogin-Welcome')

    # menu stuff
    def choose_file_to_save():
        with tk.filedialog.asksaveasfile(initialdir='.', defaultextension=".txt", filetypes=(("Text files", "*.txt;"), ("All files", "*.*"))) as f:
            print(f.write('Something random to read.\nand something else random to read.'))

            sav = messagebox.showinfo("Information", "File saved successfully")

    def choose_file_to_open():
        with tk.filedialog.askopenfile(initialdir='.', filetypes=(
                ("Text files", "*.txt;"), ("XML files", "*.xml"), ("All files", "*.*"))) as f:
            fi = tk.Text(top, width=40, height=10)
            fi.grid()

            fi.insert('1.0', f'{f.read()}')

    def are_you_sure():
        if messagebox.askokcancel("Question","Do you want to quit this program?"):
            print('did it')
            LogInWindow.destroy()

    menu = tk.Menu(top)
    top.config(menu=menu)
    filemenu = tk.Menu(menu)

    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Open", command=choose_file_to_open)
    filemenu.add_command(label="Save", command=choose_file_to_save)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=lambda: are_you_sure())
    top.mainloop()


LogInWindow.mainloop()
