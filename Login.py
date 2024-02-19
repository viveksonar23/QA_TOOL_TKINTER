import subprocess
import time
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector as mysql

def show_message_box(title, message, delay=1500):
    messagebox.showinfo(title, message)
    root.update()
    root.after(delay, root.focus_force)

def get_database_connection(database_name):
    try:
        con = mysql.connect(host="localhost", user="root", password="", database=database_name)
        cursor = con.cursor()
        return con, cursor
    except mysql.Error as err:
        print(f"Error: {err}")
        return None, None

# Function to validate user by querying the database
def validate_user(username, password):
    con, cursor = get_database_connection("aut")
    if con and cursor:
        try:
            cursor.execute("SELECT * FROM auth WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return result is not None
        except mysql.Error as err:
            print(f"Error: {err}")
        finally:
            con.close()
    return False

def forget_password():
    root.destroy()
    subprocess.run(["python3", "Forget_Password.py"])

def open_sign_up_window():
    root.destroy()
    subprocess.run(["python3", "Register.py"])

def signin():
    global start_time
    start_time = time.time()
    entered_username = user.get()
    entered_password = code.get()

    # Check if the username is 'admin'
    if entered_username == "admin":
        if validate_user(entered_username, entered_password):
            root.destroy()
            subprocess.Popen(["python3", "Administration.py"], shell=False)
        else:
            show_message_box("Error", "Invalid Admin Username or Password!")
            user.delete(0, END)
            code.delete(0, END)
    else:
        if validate_user(entered_username, entered_password):
            root.destroy()
            show_message_box("Sign In Successful", f"Welcome, {entered_username}!")
            subprocess.Popen(["python", "MainMenu.py", entered_username], shell=False)
        else:
            show_message_box("Error", "Invalid Username or Password!")
            user.delete(0, END)
            code.delete(0, END)

def on_entry_click(event):
    if user.get() == 'Username':
        user.delete(0, END)
        user.config(fg='black')

def on_password_click(event):
    if code.get() == 'Password':
        code.delete(0, END)
        code.config(fg='black', show='*')
        
def toggle_password_visibility():
    current_show_state = code.cget("show")
    new_show_state = '' if current_show_state == '*' else '*'
    code.config(show=new_show_state)
    
# /////////////////////////////////////////////////////////////////////////
root = Tk()
root.title('QA Tool : Login')
root.geometry('1132x611+300+100')
root.configure(bg="#fff")
root.resizable(True, True)
img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
root.iconphoto(False, img)

error_message_label = Label(root, text="", fg="red")  # You can place this label where it fits best in your layout
error_message_label.pack()
# /////////////////////////////////////////////////////////////////////////

# Change this path to 'I:\\project_research\\HDET1.png' to use the other image
img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/zoomimagepeopr.png')
Label(root, image=img, bg='white').place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(root, width=350, height=320, bd=5, relief='solid', borderwidth=1)
frame.place(x=280, y=70)
frame.pack(expand=True)

heading = Label(frame, text=' User Sign In', fg='black',  font=('Arial', 19, 'bold'))
heading.place(x=100, y=5)

# Username entry
user = Entry(frame, width=25, fg='gray', font=('Microsoft YaHei UI Light', 13), bd=1, relief="solid", highlightthickness=0.5, highlightbackground="lightgray", highlightcolor="lightgray")
user.place(x=25, y=60)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_entry_click)

# Password entry with border
code = Entry(frame, width=25, fg='gray', font=('Microsoft YaHei UI Light', 13), show='*', bg='white', bd=0.5, relief='solid')
code.place(x=25, y=110)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_password_click)

# Create a variable to hold the state of the checkbox
show_password_var = IntVar()

# Checkbox to toggle password visibility with border
checkbox = ttk.Checkbutton(frame, variable=show_password_var, command=toggle_password_visibility, style="TCheckbutton")
checkbox.place(x=260, y=115)

style = ttk.Style()
style.configure("TCheckbutton", borderwidth=5, relief="solid", bd=5, highlightthickness=2, highlightbackground="black", highlightcolor="black")
# style.configure("TtokenButton", bd =4, highlightbackground = "green")

# style of the button
ttk.Style().configure("TButton", font=('Arial', 13, 'bold'), foreground='black', background='blue', borderwidth=1, relief='solid')
signin_button = ttk.Button(frame, text="Sign In", command=signin, style="TButton")
signin_button.place(x=95, y=155)

label = Label(frame, text="Don't have an Account ?", fg='black', font=('Microsoft YaHei UI Light', 13))
label.place(x=30, y=200)

# Use open_sign_up_window as the command for the "Sign up" button
ttk.Style().configure("TButton", font=('Arial', 13, 'bold'), fg='black', background='white', borderwidth=0.5, relief='solid')
sign_up = ttk.Button(frame, text="Sign Up", command=open_sign_up_window, style="TButton")
sign_up.place(x=185, y=200)

ttk.Style().configure("TButton", font=('Arial', 13, 'bold'), foreground='black', background='white', borderwidth=0.5, relief='solid')
forget_password_button = ttk.Button(frame, text="Forgot Password ?", command=forget_password, style="TButton")
forget_password_button.place(x=85, y=240)

root.mainloop()