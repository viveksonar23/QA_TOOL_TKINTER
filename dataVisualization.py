import subprocess
import tkinter as tk
from tkinter import Frame, PhotoImage, ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Wedge
import mysql.connector as mysql

class DashboardApp:
    def __init__(self, root):
        root.title("QA Tool : Data Visualization")
        root.geometry("1400x750")
        img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
        root.iconphoto(False, img)

        # Create a frame for constant buttons (Dashboard, Map)
        constant_buttons_frame = ttk.Frame(root)
        constant_buttons_frame.pack(side=tk.TOP, fill=tk.X)

        buttons = ["Dashboard", "Detection", "Stage", "Groundwater", "ET", "Flow", "Reports"]
        for button_text in buttons:
            button = ttk.Button(constant_buttons_frame, text=button_text, command=lambda t=button_text: self.show_page(t))
            button.pack(side=tk.LEFT, padx=3, pady=3)

        # Dashboard page
        self.dashboard_frame = ttk.Frame(root)
        self.dashboard_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Map page
        self.map_frame = ttk.Frame(root)
        self.map_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Stage page
        self.stage_frame = ttk.Frame(root)
        self.stage_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Filter section in the dashboard
        filter_frame = ttk.Frame(self.dashboard_frame)
        filter_frame.pack(side=tk.LEFT, padx=7, pady=7)

        filter_labels = ["QA Staff", "Recorder", "Data Types", "Report Interval", "Other Selection"]
        self.filter_menus = {}

        for label in filter_labels:
            ttk.Label(filter_frame, text=label).pack(side=tk.TOP, pady=5)
            self.filter_menus[label] = ttk.Combobox(filter_frame, values=["Option 1", "Option 2", "Option 3", "Option 4"])
            self.filter_menus[label].pack(side=tk.TOP, pady=5)

        update_button = ttk.Button(filter_frame, text="Update Graphics", style="Blue.TButton", command=self.update_graphics)
        update_button.pack(side=tk.TOP, pady=10)
        
        self.populate_qa_staff()
        
    
    def get_database_connection(self):
        try:
            con = mysql.connect(host="localhost", user="root", password="", database="aut")
            return con
        except mysql.Error as err:
            print(f"Error: {err}")
            return None

    def fetch_data_from_db(self, column_name, table_name):
        con = self.get_database_connection()
        if con is not None:
            try:
                cursor = con.cursor()
                cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name}")
                data = cursor.fetchall()
                return [item[0] for item in data]  # Assuming the column contains strings
            except mysql.Error as err:
                print(f"Error fetching data: {err}")
            finally:
                con.close()
        return []

    def populate_qa_staff(self):
        qa_staff_names = self.fetch_data_from_db("username", "auth")  # Assuming 'name' is the column name for QA staff
        self.filter_menus["QA Staff"]["values"] = qa_staff_names
        if qa_staff_names:
            self.filter_menus["QA Staff"].current(0)  # Optionally set the first item as the current item

    def show_page(self, page):
        # Hide all frames
        self.dashboard_frame.pack_forget()
        self.map_frame.pack_forget()
        self.stage_frame.pack_forget()
        # ... Hide frames for other pages similarly

        # Show the selected frame
        if page == "Dashboard":
            self.dashboard_frame.pack(side=tk.LEFT, fill=tk.Y)
        elif page == "Detection":
            self.map_frame.pack(side=tk.LEFT, fill=tk.Y)
            root.destroy()
            subprocess.Popen(["python3", "Outliers_Anomalies.py"], shell=False)
        elif page == "Stage":
            self.stage_frame.pack(side=tk.LEFT, fill=tk.Y)
        # ... Show frames for other pages similarly
        else:
            print(f"Page '{page}' not implemented yet.")

    def update_graphics(self):
        # Get selected values from dropdown menus
        qa_staff_value = self.filter_menus["QA Staff"].get()
        recorder_value = self.filter_menus["Recorder"].get()
        data_types_value = self.filter_menus["Data Types"].get()
        report_interval_value = self.filter_menus["Report Interval"].get()
        other_selection_value = self.filter_menus["Other Selection"].get()

        # Dummy data for visualization (replace with your actual data)
        assignment_categories = ["Category A", "Category B", "Category C"]
        assignment_values = [15, 25, 35]
        status_completion_value = 70  # Speedometer value
        processing_time = np.random.uniform(50, 150, size=10)  # Processing time for 10 tasks
        source_data_status_values = [30, 20, 10, 40]  # Green, Yellow, Red, Orange
        station_by_values = [10, 15, 25, 20, 30]  # Values for circular graph

        # Clear previous plots
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        def create_bordered_frame(parent, row, column, padx=(10, 10), pady=(10, 10)):
            plot_frame = Frame(parent, borderwidth=3, relief="groove", bg="black")
            plot_frame.grid(row=row, column=column, padx=padx, pady=pady)
            return plot_frame

        # Adjusted to include plot creation inside a bordered frame
        def create_plot(fig, master, row, column):
            canvas = FigureCanvasTkAgg(fig, master=master)
            widget = canvas.get_tk_widget()
            widget.pack(fill=tk.BOTH, expand=True)
            return canvas


        # Create Assignment Bar Plot
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.bar(assignment_categories, assignment_values, color=['blue', 'green', 'orange'])
        ax1.set_title("Assignment")
        bordered_frame1 = create_bordered_frame(self.dashboard_frame, 0, 0)
        create_plot(fig1, bordered_frame1, 0, 0)

        # Create Status Completion Speedometer
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.set_xlim(0, 100)
        ax2.set_ylim(0, 100)
        ax2.add_patch(Wedge((50, 50), 45, 0, status_completion_value, color='green', alpha=0.7))
        ax2.set_title("Status Completion")
        bordered_frame2 = create_bordered_frame(self.dashboard_frame, 0, 1)
        create_plot(fig2, bordered_frame2, 0, 1)

        # Create Processing Time Plot
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.plot(processing_time, marker='o', color='dodgerblue')
        ax3.set_title("Processing Time", fontsize=10)
        ax3.grid(True, which='both', linestyle='--', linewidth=0.5)
        bordered_frame3 = create_bordered_frame(self.dashboard_frame, 0, 2)
        create_plot(fig3, bordered_frame3, 0, 2)


        # Create Source Data Status Horizontal Bar Graph
        fig4, ax4 = plt.subplots(figsize=(4, 3))
        ax4.barh(["Green", "Yellow", "Red", "Orange"], source_data_status_values, color=['green', 'yellow', 'red', 'orange'])
        ax4.set_title("Data Status", fontsize=10)
        bordered_frame4 = create_bordered_frame(self.dashboard_frame, 1, 0)
        create_plot(fig4, bordered_frame4, 1, 0)


        # Create Station By Circular Graph
        fig5, ax5 = plt.subplots(figsize=(4, 3))
        ax5.pie(station_by_values, labels=['1', '2', '3', '4', '5'], autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange', 'lightgreen', 'yellow', 'violet'])
        ax5.set_title("Stations", fontsize=10)
        bordered_frame5 = create_bordered_frame(self.dashboard_frame, 1, 1)
        create_plot(fig5, bordered_frame5, 1, 1)


        # Create a duplicate of Processing Time Plot for the sixth section
        fig6, ax6 = plt.subplots(figsize=(4, 3))
        ax6.plot(processing_time, marker='o', color='dodgerblue')
        ax6.set_title("Processing Time Duplicate", fontsize=10)
        ax6.grid(True, which='both', linestyle='--', linewidth=0.5)
        bordered_frame6 = create_bordered_frame(self.dashboard_frame, 1, 2)
        create_plot(fig6, bordered_frame6, 1, 2)


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()