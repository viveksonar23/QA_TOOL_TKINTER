import tkinter as tk
from tkinter import END, WORD, Label, PhotoImage, Text, Toplevel, ttk, messagebox
from datetime import datetime
import time
import subprocess
import sys
import mysql.connector as mysql
start_time = None
    
def check_for_new_tasks(username):
    # Example query to check for new tasks; modify as needed
    query = "SELECT COUNT(*) FROM insertalldata WHERE username=%s AND task=True"
    tasks_cursor.execute(query, (username,))
    result = tasks_cursor.fetchone()
    return result[0] > 0

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

tasks_db = mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="stationandusermain"
)
tasks_cursor = tasks_db.cursor()

def logout():
    global start_time
    if start_time is not None:
        # Ask for confirmation
        confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?")
        if confirm:
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_minutes = int(elapsed_time // 60)
            elapsed_time_seconds = int(elapsed_time % 60)
            total_time_spent = f"Total Time Spent: {elapsed_time_minutes} minutes {elapsed_time_seconds} seconds"
            show_message_box("Time Spent", f"Total Time Spent: {elapsed_time_minutes} minutes {elapsed_time_seconds} seconds")
            
            with open("total_time_spent.txt", "a") as file:
                file.write(f"{datetime.now()} - {total_time_spent}\n")
            
            root.destroy()
            subprocess.Popen(["python", "Login.py"], shell=False)
            
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = None

def task():
    if username:
        new_task = check_for_new_tasks(username)
        if new_task:
            task_btn.config(text="New Tasks!", style="NewTask.TButton")
        else:
            task_btn.config(text="Task", style="TButton")
        show_tasks(username)
    else:
        show_message_box("Error", "No username provided.")
        
def manage_tasks():
    manage_tasks_window = Toplevel(root)
    manage_tasks_window.title("Manage Tasks")
    manage_tasks_window.geometry("1132x611+300+100")  # Adjust the size as needed

    # Button for Task Manager
    task_manager_btn = ttk.Button(manage_tasks_window, text="Task Manager", command=task_manager)
    task_manager_btn.pack(pady=10)

    # Button for Manage the Task
    manage_task_btn = ttk.Button(manage_tasks_window, text="Assign Task", command=manage_task)
    manage_task_btn.pack(pady=10)

def task_manager():
    subprocess.Popen(["python3", "TaskManager.py"], shell=False)

def manage_task():
    subprocess.Popen(["python3", "AssignStations.py"], shell=False)

def on_closing():
    global start_time
    if start_time is not None:
        end_time = time.time()
        elapsed_time = end_time - start_time

        start_datetime_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_datetime_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

        elapsed_time_hours = int(elapsed_time // 3600)
        elapsed_time_remaining_secs = int(elapsed_time % 3600)
        elapsed_time_minutes = elapsed_time_remaining_secs // 60
        elapsed_time_seconds = elapsed_time_remaining_secs % 60

        session_details = (
            f"Login: {start_datetime_str}, "
            f"Logout: {end_datetime_str}, "
            f"Total Time Spent: {elapsed_time_hours} hours, {elapsed_time_minutes} minutes, {elapsed_time_seconds} seconds"
        )

        # Log the session details to a file
        with open("session_log.txt", "a") as file:
            file.write(f"{session_details}\n")
        
        # Confirm logout and exit
        confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?")
        if confirm:
            root.destroy()
            subprocess.Popen(["python", "Login.py"], shell=False)
    else:
        # Handle case where start_time is None (e.g., if the application is closed without properly logging in)
        root.destroy()

# Make sure to call on_main_window_open somewhere to set start_time, such as binding it to the window's open event or calling it directly in your script.

def on_main_window_open(event):
    global start_time
    start_time = time.time()  # Record start time
    # update_running_time(root, running_time_label)  # Start updating running time

def update_running_time(main_window, label):
    global start_time
    if start_time is not None:
        current_time = time.time()
        elapsed_time = current_time - start_time
        elapsed_time_minutes = int(elapsed_time // 60)
        elapsed_time_seconds = int(elapsed_time % 60)
        label.config(text=f"Running Time: {elapsed_time_minutes:02d}:{elapsed_time_seconds:02d}")
        main_window.after(1000, update_running_time, main_window, label)  # Schedule the function to run again after 1000 milliseconds

def data_retrieval():
    subprocess.Popen(["python3", "final_dashboard_Integrated.py"], shell=False)

def data_assessment():
    subprocess.Popen(["python3", "Outliers_Anomalies.py"], shell=False)

def report():
    subprocess.Popen(["python3", "userMaintenanceReport.py"], shell=False)

def help():
    subprocess.Popen(["python3", "Help.py"], shell=False)

def about():
    subprocess.Popen(["python3", "About.py"], shell=False)
    
def data_visualization():
    subprocess.Popen(["python3", "dataVisualization.py"], shell=False)
    
def show_tasks(username):
    con, cursor = get_database_connection("stationandusermain")
    if not con or not cursor:
        show_message_box("Error", "Failed to connect to the tasks database.")
        return

    employee_window = Toplevel()
    employee_window.title(f"Tasks Assigned to {username}")
    employee_window.geometry("1000x600")

    # Frame for tasks
    tasks_frame = ttk.Frame(employee_window)
    tasks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Scrollbar for the Text widget
    scrollbar = ttk.Scrollbar(tasks_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Text widget for tasks with a Scrollbar
    tasks_text = tk.Text(tasks_frame, wrap=tk.WORD, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
    tasks_text.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=tasks_text.yview)

    query = "SELECT * FROM insertalldata WHERE username=%s"
    cursor.execute(query, (username,))
    tasks = cursor.fetchall()

    # Number the tasks and insert into the Text widget
    for i, task in enumerate(tasks, start=1):
        task_str = f"Task {i}:\n    Station: {task[0]}\n    DBkey: {task[1]}\n    Data type: {task[2]}\n    Eff date: {task[3]}\n    QA interval: {task[5]}\n    Report group: {task[6]}\n    Budget code: {task[7]}\n    Mandate: {task[8]}\n    EE grade: {task[9]}\n    HRS PER YEAR: {task[10]}\n    Customer POC: {task[11]}\n    Comments: {task[12]}\n    General Information Notes:{task[13]}\n    Task: {task[14]}\n    Deadline: {task[15]}\n\n"
        tasks_text.insert(tk.END, task_str)

    # Make the text widget read-only
    tasks_text.config(state=tk.DISABLED)

    cursor.close()
    con.close()
    
    
def show_assigned_tasks():
    if username:
        new_task = check_for_new_tasks(username)
        if new_task:
            show_assigned_tasks.config(text="New Tasks!", style="NewTask.TButton")
        else:
            show_assigned_tasks.config(text="Task", style="TButton")
        show_tasks(username)
    else:
        show_message_box("Error", "No username provided.")
    
def fetch_assigned_tasks(username):
    con, cursor = get_database_connection("stationandusermain")
    if con and cursor:
        try:
            cursor.execute("SELECT * FROM insertalldata WHERE username=%s", (username,))
            tasks = cursor.fetchall()
            return tasks
        except mysql.Error as err:
            print(f"Error fetching assigned tasks: {err}")
        finally:
            con.close()
    return []
    
def update_task_button():
    if username:
        new_task = check_for_new_tasks(username)
        if new_task:
            # Adding a notification symbol (*) and changing the text color to white
            task_btn.config(text="Tasks *", style="NewTask.TButton")
        else:
            task_btn.config(text="Tasks", style="TButton")
    root.after(60000, update_task_button)  # Check every 60 seconds

root = tk.Tk()
root.title('QA Tool : Main Menu')
root.geometry('1132x611+300+100')  # Increased size
root.configure(bg="#fff")
root.resizable(True, True)
img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
root.iconphoto(False, img)

# Add a dark border to the main frame
button_frame = ttk.Frame(root, padding=(40, 40, 40, 40), borderwidth=2, relief='solid')
button_frame.place(relx=0.5, rely=0.5, anchor="center")

ttk.Style().configure("TButton", font=('Arial', 14, 'bold'), fg='white', background='#4CAF50', borderwidth=2, relief='solid')

data_retrieval_btn = ttk.Button(button_frame, text="Data Retrieval", style="TButton", command=data_retrieval)
data_retrieval_btn.grid(row=0, column=0, pady=10, padx=15)

data_visualization_btn = ttk.Button(button_frame, text="Data Visualization", style="TButton", command = data_visualization)
data_visualization_btn.grid(row=0, column=1, pady=10, padx=15)

data_assessment_btn = ttk.Button(button_frame, text="Data Assessment", style="TButton", command=data_assessment)
data_assessment_btn.grid(row=0, column=2, pady=10, padx=15)

report_btn = ttk.Button(button_frame, text="Reports", style="TButton", command=report)
report_btn.grid(row=1, column=0, pady=10, padx=15)

help_btn = ttk.Button(button_frame, text="Help", style="TButton", command=help)
help_btn.grid(row=1, column=1, pady=10, padx=15)

about_btn = ttk.Button(button_frame, text="About", style="TButton", command=about)
about_btn.grid(row=1, column=2, pady=10, padx=15)

ttk.Style().configure("NewTask.TButton", font=('Arial', 14, 'bold'), fg='white', background='red', borderwidth=2, relief='solid')
task_btn = ttk.Button(button_frame, text="Assigned Task", style="TButton", command = task)
task_btn.grid(row=2, column=1, pady=20, padx=15)

logout_btn = ttk.Button(button_frame, text="Logout", style="TButton", command=logout)
logout_btn.grid(row=3, column=1, pady=20, padx=15)

# running_time_label = Label(root, text="Running Time: 0:00", fg='black', bg='#3498db', font=('Arial', 15), bd=1, relief='solid')
# running_time_label.place(relx=1.0, x=-20, y=20, anchor="ne")

manage_tasks_btn = ttk.Button(button_frame, text="Manage Tasks", style="TButton", command=manage_tasks)
manage_tasks_btn.grid(row=2, column=2, pady=20, padx=15)

update_task_button()

# Bind the <Configure> event to on_main_window_open
root.bind("<Configure>", on_main_window_open)

root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind the close event to custom function

root.mainloop()