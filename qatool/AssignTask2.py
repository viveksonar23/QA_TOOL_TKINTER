import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import messagebox
import mysql.connector as mysql

def get_database_connection():
    try:
        con = mysql.connect(host="localhost", user="root", password="", database="aut")
        cursor = con.cursor()
        return con, cursor
    except mysql.Error as err:
        print(f"Error: {err}")
        return None, None

def fetch_data_from_db(table_name, column_name):
    con, cursor = get_database_connection()
    if con and cursor:
        try:
            cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name}")
            data = cursor.fetchall()
            return [item[0] for item in data]
        except mysql.Error as err:
            print(f"Error: {err}")
        finally:
            con.close()
    return []

class TaskManagerApp:
    def __init__(self, root):
        root.title("QA Tool : Assign Task")
        root.geometry("1132x611+300+100")
        img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
        root.iconphoto(False, img)

        # Configure ttk style
        self.style = ttk.Style()
        self.style.configure("TEntry", borderwidth=2, relief="solid")  # Set borderwidth and relief for TEntry

        self.tasks = []

        # Fetch employees from database
        employees_list = fetch_data_from_db("auth", "username")  # Replace with your table and column name
        self.employees = {name: {"tasks": []} for name in employees_list}

        self.task_frame = ttk.Frame(root)
        self.task_frame.pack(pady=10)

        self.task_label = ttk.Label(self.task_frame, text="Task:")
        self.task_label.grid(row=0, column=0, padx=5)

        self.task_entry = ttk.Entry(self.task_frame, width=30, style="TEntry")  # Apply style to the entry
        self.task_entry.grid(row=0, column=1, padx=5)

        self.employee_label = ttk.Label(self.task_frame, text="Assign to Employee:")
        self.employee_label.grid(row=0, column=2, padx=5)

        self.employee_combobox = ttk.Combobox(self.task_frame, values=employees_list, state="readonly")
        self.employee_combobox.grid(row=0, column=3, padx=5)

        self.add_button = ttk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=4, padx=5)

        self.task_tree_frame = ttk.Frame(root)
        self.task_tree_frame.pack(pady=10)

        self.task_tree = ttk.Treeview(self.task_tree_frame, columns=("Task", "Assigned To"))
        self.task_tree.grid(row=0, column=0)

        self.task_tree.heading("#0", text="ID")
        self.task_tree.heading("Task", text="Task")
        self.task_tree.heading("Assigned To", text="Assigned To")

    def add_task(self):
        task_text = self.task_entry.get()
        assigned_to = self.employee_combobox.get()

        if task_text and assigned_to:
            task_id = len(self.tasks) + 1
            self.tasks.append({"id": task_id, "task": task_text, "assigned_to": assigned_to})
            self.employees[assigned_to]["tasks"].append({"id": task_id, "task": task_text})
            self.update_task_tree()
            self.clear_entry_fields()
            self.notify_employee(assigned_to, task_text)

    def update_task_tree(self):
        self.task_tree.delete(*self.task_tree.get_children())
        for task in self.tasks:
            self.task_tree.insert("", "end", text=task["id"], values=(task["task"], task["assigned_to"]))

    def clear_entry_fields(self):
        self.task_entry.delete(0, "end")
        self.employee_combobox.set("")

    def notify_employee(self, employee, task):
        messagebox.showinfo("Task Assigned", f"A new task has been assigned to you: {task}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
