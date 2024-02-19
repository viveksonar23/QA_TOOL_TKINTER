import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to the 'signin' database for login information
login_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="signin"
)
login_cursor = login_db.cursor()

# Connect to the 'your_other_database' database for tasks
tasks_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stationandusermain"
)
tasks_cursor = tasks_db.cursor()

class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x1000")
        self.root.title("Task Management")

        # self.username_label = tk.Label(root, text="Username:")
        # self.username_label.pack()
        # self.username_entry = tk.Entry(root)
        # self.username_entry.pack()

        # self.password_label = tk.Label(root, text="Password:")
        # self.password_label.pack()
        # self.password_entry = tk.Entry(root, show="*")
        # self.password_entry.pack()

        # self.login_button = tk.Button(root, text="Login", command=self.login)
        # self.login_button.pack()

    # def login(self):
    #     username = self.username_entry.get()
    #     password = self.password_entry.get()

    #     # Query the 'signin' database for the provided username and password
    #     query = "SELECT * FROM validate WHERE username=%s AND password=%s"
    #     login_cursor.execute(query, (username, password))
    #     result = login_cursor.fetchone()

    #     if result:
    #         self.show_tasks(username)
    #     else:
    #         messagebox.showerror("Error", "Invalid username or password")

    def show_tasks(self, username):
        self.root.destroy()

        employee_window = tk.Tk()
        
        employee_window.title(f"Tasks for {username}")
        employee_window.geometry("1000x1000")

        # Query the 'your_other_database' database for tasks related to the given username
        query = "SELECT * FROM insertalldata WHERE username=%s"
        tasks_cursor.execute(query, (username,))
        tasks = tasks_cursor.fetchall()

        tasks_label = tk.Label(employee_window, text="Tasks:", font=("Helvetica", 16))

        tasks_label.pack()

        tasks_listbox = tk.Listbox(employee_window)
        for task in tasks:
            tasks_listbox.insert(tk.END, f"Station: {task[0]}\n DBkey: {task[1]}\n Data type: {task[2]}\n Eff date: {task[3]}\n QA interval: {task[5]}\n Report group: {task[6]}\n Budget code: {task[7]}\n Mandate: {task[8]}\nEE grade: {task[9]}\n HRS PER YEAR: {task[10]}\n Customer POC: {task[11]}\n Comments: {task[12]}\n General Information Notes:{task[13]}\n Task : {task[14]}\n Deadline : {task[15]}\n")
        tasks_listbox.pack()

        employee_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()
