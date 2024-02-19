from tkinter import *
from tkinter import ttk, messagebox
import os
import subprocess
import tkinter
import mysql.connector as mysql

root = Tk()
root.title('QA Tool : Registration')
root.geometry('1132x611+300+100')
root.configure(bg="#fff")
root.resizable(True, True)
img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
root.iconphoto(False, img)
     
bg_img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/zoomimagepeopr.png')
bg_label = Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

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

def validate_user(first_name, last_name):
    con, cursor = get_database_connection()
    if con and cursor:
        try:
            cursor.execute("SELECT * FROM authorizeuser WHERE first_name = %s AND last_name = %s", (first_name, last_name))
            result = cursor.fetchone()
            return result is not None
        except mysql.Error as err:
            print(f"Error: {err}")
        finally:
            con.close()

    return False

def register_page():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    username = username_entry.get()
    security_question = security_question_combobox.get()
    security_answer = security_answer_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if len(first_name) == 0 or len(last_name) == 0 or len(username) == 0 or len(security_question) == 0 or len(security_answer) == 0 or len(password) == 0 or len(confirm_password) == 0:
       show_message_box("Error", "All fields are required!")
    elif password != confirm_password:
        show_message_box("Error", "Passwords do not match!")
    elif not validate_user(first_name, last_name):
        show_message_box("Error", "Invalid first name or last name!")
    else:
        con = mysql.connect(host="localhost", user ="root", password = "", database = "aut")
        cursor = con.cursor()
       
        cursor.execute("INSERT INTO auth VALUES(%s, %s, %s, %s, %s, %s)", (first_name, last_name, username, password, security_question, security_answer))
        cursor.execute("commit")
        con.close()
        
        root.destroy()
        show_message_box("Registration Successful", f"Registration Successful!\nWelcome, {first_name} {last_name}!")
        subprocess.Popen(["python3", "Login.py"], shell=False)
        root.destroy()

# Create a frame for user sign-up
signup_frame = ttk.Frame(root, padding=10, relief='solid', borderwidth=1)
signup_frame.place(x=400, y=150)
signup_frame.pack(expand=True)

heading = Label(signup_frame, text='User Sign Up', font=('Arial', 20, 'bold'))
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

label_username = Label(signup_frame, text='Create Username', font=('Microsoft YaHei UI Light', 15))
label_username.grid(row=3, column=0, pady=5, sticky='e')

username_entry = Entry(signup_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid", highlightthickness=0.5, highlightbackground="lightgray", highlightcolor="lightgray")
username_entry.grid(row=3, column=1, pady=5, padx=5)

# Add "Security Question" combobox
label_security_question = Label(signup_frame, text='Security Questions', font=('Microsoft YaHei UI Light', 15))
label_security_question.grid(row=6, column=0, padx=5, pady=5, sticky='e')

security_questions = ["What is the name of your first car?", "Which Elementry school you attended?"]
security_question_combobox = ttk.Combobox(signup_frame, values=security_questions, width=30, font=('Microsoft YaHei UI Light', 15), state="readonly")
security_question_combobox.grid(row=6, column=1, pady=6, padx=6)

# Entry for security answer
label_security_answer = Label(signup_frame, text='Security Answer', font=('Microsoft YaHei UI Light', 15))
label_security_answer.grid(row=7, column=0, pady=5, sticky='e')

security_answer_entry = Entry(signup_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid", highlightthickness=0.5, highlightbackground="lightgray", highlightcolor="lightgray")
security_answer_entry.grid(row=7, column=1, pady=5, padx=5)

label_password = Label(signup_frame, text='Create Password', font=('Microsoft YaHei UI Light', 15))
label_password.grid(row=4, column=0, pady=5, sticky='e')

password_entry = Entry(signup_frame, width=30, font=('Microsoft YaHei UI Light', 15), show='*', bd=1, relief="solid", highlightthickness=0.5, highlightbackground="lightgray", highlightcolor="lightgray")
password_entry.grid(row=4, column=1, pady=5, padx=5)

label_confirm_password = Label(signup_frame, text='Confirm Password', font=('Microsoft YaHei UI Light', 15))
label_confirm_password.grid(row=5, column=0, pady=5, sticky='e')

confirm_password_entry = Entry(signup_frame, width=30, font=('Microsoft YaHei UI Light', 15), show='*', bd=1, relief="solid", highlightthickness=0.5, highlightbackground="lightgray", highlightcolor="lightgray")
confirm_password_entry.grid(row=5, column=1, pady=5, padx=5)

ttk.Style().configure("TButton", padding=6, relief="flat", background="gray", foreground="black", borderwidth=5, highlightbackground="black", highlightcolor="black", font=('Arial', 13, 'bold'))
register_button = ttk.Button(signup_frame, text="Register", command=register_page, style="TButton")
register_button.grid(row=8, column=1, pady=10)

root.mainloop()