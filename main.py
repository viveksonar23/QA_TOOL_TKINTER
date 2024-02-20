import subprocess
import time
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as mysql
from qatool.Login import LoginScreen
from qatool.Forget_Password import PasswordResetApp
from qatool.Register import RegisterScreen

class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self)  
        self.geometry('1132x611+300+100')
        self.configure(bg="#fff")
        self.resizable(True, True)
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (RegisterScreen, PasswordResetApp, LoginScreen):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(LoginScreen)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

app = tkinterApp()
app.mainloop()
