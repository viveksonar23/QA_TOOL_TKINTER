import subprocess
import time
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector as mysql
from Login import LoginScreen


root = Tk()
root.title('QA Tool : Login')
root.geometry('1132x611+300+100')
root.configure(bg="#fff")
root.resizable(True, True)
img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
root.iconphoto(False, img)

root.mainloop()