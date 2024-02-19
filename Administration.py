import tkinter as tk
from tkinter import Entry, Frame, Label, Button, PhotoImage, Toplevel
import subprocess

def create_account(user_type):
    # Function to handle the creation of a new account
    def save_account():
        if user_type == "admin":
            # Additional fields for admin
            first_name_value = first_name_entry.get()
            last_name_value = last_name_entry.get()
            print(f"New {user_type.capitalize()} User Creation Sucessfully!:")
            print(f"First Name: {first_name_value}")
            print(f"Last Name: {last_name_value}")
            
        else:
            username_value = username_entry.get()
            password_value = password_entry.get()
            print(f"New {user_type.capitalize()} Sign In Succesfully!:")
            print(f"Username: {username_value}")
            print(f"Password: {password_value}")

        new_account_window.destroy()

    # Create a new window for creating an account
    new_account_window = Toplevel(root)
    new_account_window.title(f"Create {user_type.capitalize()} Account")

    if user_type== "user":
        # Create labels and entry widgets for username and password
        Label(new_account_window, text="Username:").pack(pady=5)
        username_entry = Entry(new_account_window)
        username_entry.pack(pady=5)

        Label(new_account_window, text="Password:").pack(pady=5)
        password_entry = Entry(new_account_window, show="*")
        password_entry.pack(pady=5)
        
        
        save_button = Button(new_account_window, text="Sign In", command=save_account)
        save_button.pack(pady=10)
        
    if user_type == "admin":
    # Additional fields for admin
        Label(new_account_window, text="First Name:").pack(pady=5)
        first_name_entry = Entry(new_account_window)
        first_name_entry.pack(pady=5)

        Label(new_account_window, text="Last Name:").pack(pady=5)
        last_name_entry = Entry(new_account_window)
        last_name_entry.pack(pady=5)

        # Create a button to save the account
        save_button = Button(new_account_window, text="create User", command=save_account)
        save_button.pack(pady=10)

# Function to handle user login
def user_login():
    subprocess.Popen(["python3", "Login.py"], shell=False)

# Function to handle admin login
def admin_login():
    subprocess.Popen(["python3", "UserCreation.py"], shell=False)

# Create the main window
root = tk.Tk()
root.title("QA Tool : Administration Control")
root.geometry('1132x611+300+100')
img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
root.iconphoto(False, img)

# # Change this path to 'I:\\project_research\\HDET1.png' to use the other image
# img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/zoomimagepeopr.png')
# Label(root, image=img, bg='white').place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(root, width=350, height=320)
frame.place(x=280, y=70)
frame.pack(expand=True)

# Create a button for user login
user_button = Button(frame, text="QA Tool", command=user_login, height=3, width=20, font=('Arial', 16, 'bold'), bd=0.5, highlightbackground='black', highlightcolor='black')
user_button.pack(pady=10)
user_button.pack(expand=True)

# Create a button for admin login
admin_button = Button(frame, text="User Creation", command=admin_login, height=3, width=20, font=('Arial', 16, 'bold'),bd=0.5, highlightbackground='black', highlightcolor='black')
admin_button.pack(pady=10)
admin_button.pack(expand=True)

# Run the main loop
root.mainloop()