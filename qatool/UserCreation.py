from tkinter import *
from tkinter import ttk, messagebox
import os
import subprocess
import mysql.connector as mysql


def show_message_box(title, message, delay=1500):
    messagebox.showinfo(title, message)
    root.update()
    root.after(delay, root.focus_force)

def get_database_connection():
    try:
        con = mysql.connect(host="localhost", user="root", password="", database="registerauth")
        cursor = con.cursor()
        return con, cursor
    except mysql.Error as err:
        print(f"Error: {err}")
        return None, None

def forget_password():
    root.withdraw()
    subprocess.Popen(["python3", "Forget_Password.py"], shell=False)

def createUsers():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    if len(first_name) == 0 or len(last_name) == 0:
        show_message_box("Error", "All fields are required!")
    else:
        con = mysql.connect(host="localhost", user ="root", password = "", database = "registerauth")
        cursor = con.cursor()
        cursor.execute("INSERT INTO authorizeuser VALUES(%s, %s)", (first_name, last_name))
        cursor.execute("commit")
        con.close()
        
        show_message_box("User creation Successfully", f"User Creation Successful!\n{first_name} {last_name}!")
        root.withdraw()

root = Tk()
root.title('QA Tool : User Creation')
root.geometry('1132x611+300+100')
root.configure(bg="#fff")
root.resizable(True, True)
img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
root.iconphoto(False, img)

bg_img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/zoomimagepeopr.png')
bg_label = Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for user sign-up
signup_frame = ttk.Frame(root, padding=10, relief='solid', borderwidth=1)
signup_frame.place(x=400, y=150)
signup_frame.pack(expand=True)

heading = Label(signup_frame, text='User Creation', font=('Arial', 20, 'bold'))
heading.place(x=300, y=4)
heading.grid(row=0, column=0, columnspan=5,padx=10, pady=10)

label_first_name = Label(signup_frame, text='First Name', font=('Microsoft YaHei UI Light', 15))
label_first_name.grid(row=1, column=0, pady=5, sticky='e')

first_name_entry = Entry(signup_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid", highlightthickness=0.5, highlightbackground="lightgray", highlightcolor="lightgray")
first_name_entry.grid(row=1, column=1, pady=5, padx=5)

label_last_name = Label(signup_frame, text='Last Name', font=('Microsoft YaHei UI Light', 15))
label_last_name.grid(row=2, column=0, pady=5, sticky='e')

last_name_entry = Entry(signup_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid", highlightthickness=0.5, highlightbackground="lightgray", highlightcolor="lightgray")
last_name_entry.grid(row=2, column=1, pady=5, padx=5)

ttk.Style().configure("TButton", padding=6, relief="flat", background="gray", foreground="black", borderwidth=5, highlightbackground="black", highlightcolor="black", font=('Arial', 13, 'bold'))
register_button = ttk.Button(signup_frame, text="Create User", command=createUsers, style="TButton")
register_button.grid(row=8, column=1, pady=10)

ttk.Style().configure("TButton", font=('Arial', 13, 'bold'), foreground='black', background='white', borderwidth=0.5, relief='solid')
forget_password_button = ttk.Button(signup_frame, text="Forgot Password ?", command=forget_password, style="TButton")
forget_password_button.grid(row=9, column=1, pady=10)

root.mainloop()