from logging import root
import subprocess
import time
import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector as mysql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geopandas as gpd

def get_database_connection():
    try:
        con = mysql.connect(host="localhost", user="root", password="", database="stationandusermain")
        cursor = con.cursor()
        return con, cursor
    except mysql.Error as err:
        print(f"Error: {err}")
        return None, None

def fetch_data_from_db(column_name, table_name):
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

def get_database_connection1():
    try:
        con = mysql.connect(host="localhost", user="root", password="", database="aut")
        cursor = con.cursor()
        return con, cursor
    except mysql.Error as err:
        print(f"Error: {err}")
        return None, None

def fetch_data_from_db1(column_name1, table_name):
    con, cursor = get_database_connection1()
    if con and cursor:
        try:
            cursor.execute(f"SELECT DISTINCT {column_name1} FROM {table_name}")
            data = cursor.fetchall()
            # Concatenate the two columns into a single string
            return [f"{item[0]}" for item in data]
        except mysql.Error as err:
            print(f"Error: {err}")
        finally:
            con.close()
    return []

class StationUserMaintenance(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QA Tool : User Assignment (Administrator)")
        self.geometry("1200x800")
        img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
        self.iconphoto(False, img)    

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        right_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        headline_label = tk.Label(left_frame, text="User Assignment", font=("Helvetica", 16))
        headline_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        tk.Label(left_frame, text="Station").grid(row=1, column=0, sticky=tk.W)  # Adjust alignment to West (tk.W)
        self.station_listbox = tk.Listbox(left_frame, selectmode='extended', exportselection=0, height=4)  # Set height as needed
        self.station_listbox.grid(row=1, column=1, padx=5, pady=5, sticky='ew')  # Make it fill the cell in East-West direction
        
        station_scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=self.station_listbox.yview)
        station_scrollbar.grid(row=1, column=2, sticky='ns')
        self.station_listbox.configure(yscrollcommand=station_scrollbar.set)

        stations = fetch_data_from_db("Station", "station")
        for station in stations:
            self.station_listbox.insert(tk.END, station)

        tk.Label(left_frame, text="DBkey").grid(row=2, column=0, sticky=tk.E)
        self.dbkey_var = tk.StringVar()
        dbkey_menu = ttk.Combobox(left_frame, textvariable=self.dbkey_var, state="readonly")  # Use ttk.Combobox
        dbkey_menu.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Data type").grid(row=3, column=0, sticky=tk.E)
        self.data_type_var = tk.StringVar()
        data_type_menu = ttk.Combobox(left_frame, textvariable=self.data_type_var, state="readonly")  # Use ttk.Combobox
        data_type_menu.grid(row=3, column=1, padx=5, pady=5)

        # Individual Entry widgets
        tk.Label(left_frame, text="Effective date").grid(row=4, column=0, sticky=tk.E)
        self.eff_date_entry = DateEntry(left_frame, date_pattern='yyyy-mm-dd', show_week_numbers=True, show_other_months=True, year_range=(2021, 2025))
        self.eff_date_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="username").grid(row=5, column=0, sticky=tk.E)
        self.username_var = tk.StringVar()
        username_combobox = ttk.Combobox(left_frame, textvariable=self.username_var, state="readonly")
        username_combobox.grid(row=5, column=1, padx=5, pady=5)
        
        # Fetch data from the database and populate ComboBoxes
        # station_menu['values'] = fetch_data_from_db("Station", "station")
        dbkey_menu['values'] = fetch_data_from_db("DBkey", "dbkey")
        data_type_menu['values'] = fetch_data_from_db("DataType", "datatype")
        username_combobox['values'] = fetch_data_from_db1("username", "auth")

        tk.Label(left_frame, text="QA Interval").grid(row=6, column=0, sticky=tk.E)
        self.qa_interval_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.qa_interval_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Report Group").grid(row=7, column=0, sticky=tk.E)
        self.report_group_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.report_group_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Budget Code").grid(row=8, column=0, sticky=tk.E)
        self.budget_code_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.budget_code_entry.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Mandate").grid(row=9, column=0, sticky=tk.E)
        self.mandate_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.mandate_entry.grid(row=9, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="EE grade").grid(row=10, column=0, sticky=tk.E)
        self.ee_grade_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.ee_grade_entry.grid(row=10, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="HOURS PER YEAR").grid(row=11, column=0, sticky=tk.E)
        self.hrs_per_year_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.hrs_per_year_entry.grid(row=11, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Customer POC").grid(row=12, column=0, sticky=tk.E)
        self.customer_poc_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.customer_poc_entry.grid(row=12, column=1, padx=5, pady=5)

        # Comments and General Information Notes
        comments_label = tk.Label(left_frame, text="Comments:")
        comments_label.grid(row=13, column=0, sticky=tk.E)
        self.comments_text = tk.Text(left_frame, height=5, width=30,highlightthickness=1, highlightbackground="black")
        self.comments_text.grid(row=13, column=1, columnspan=2, padx=5, pady=5)

        general_info_label = tk.Label(left_frame, text="General Information Notes:")
        general_info_label.grid(row=14, column=0, sticky=tk.E)
        self.general_info_text = tk.Text(left_frame, height=5, width=30, highlightthickness=1, highlightbackground="black")
        self.general_info_text.grid(row=14, column=1, columnspan=2, padx=5, pady=5)
        
        tk.Label(left_frame, text="Task : ").grid(row=15, column=0, sticky=tk.E)
        self.task_entry = tk.Entry(left_frame, highlightthickness=1, highlightbackground="black")
        self.task_entry.grid(row=15, column=1, padx=5, pady=5)

        # Deadline Calendar
        tk.Label(left_frame, text="Deadline : ").grid(row=16, column=0, sticky=tk.E)
        self.deadline_entry = DateEntry(left_frame, date_pattern='yyyy-mm-dd', show_week_numbers=True, show_other_months=True, year_range=(2021, 2025))
        self.deadline_entry.grid(row=16, column=1, padx=5, pady=5)

        # Button for saving changes
        save_changes_button = tk.Button(left_frame, text="Save and Assign", command=self.save_changes)
        save_changes_button.grid(row=17, column=0, columnspan=3, pady=10)
        
        self.setup_left_frame(left_frame)
        self.plot_shapefile(right_frame)
        
    def on_station_select(self, event=None):
        selected_indices = self.station_listbox.curselection()
        if not selected_indices:
            return
        selected_station = self.station_listbox.get(selected_indices[0])
        lat, lon = self.fetch_station_coordinates(selected_station)
        if lat is not None and lon is not None:
            # Clear the existing plot
            self.ax.clear()
            # Plot the new point
            self.ax.scatter(lon, lat, color='red', marker='o', label=selected_station)
            # You might want to re-plot other elements here, like the shapefile boundary
            self.gdf.boundary.plot(ax=self.ax, color='black', linewidth=1)
            # Refresh the canvas
            self.canvas.draw()
        else:
            print("Coordinates not found for the selected station.")
        
    def plot_shapefile(self, shapefile_frame):
        fig, ax = plt.subplots(figsize=(4, 4))
        self.canvas = FigureCanvasTkAgg(fig, master=shapefile_frame)  # Store the canvas as an instance variable for later access
        self.canvas.get_tk_widget().pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        gdf = gpd.read_file("/Users/viveksonar/Desktop/project_research_4/Floridafile/FloridaShapeFile.shp")
        
        # Plot only the boundary of the shapefile
        gdf.boundary.plot(ax=ax, color='black', linewidth=1)
        
        # Set titles and labels (optional, but good practice)
        # ax.set_title("Shapefile Boundary Plot")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        
        # Adding a grid
        ax.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5)
        
        # Store gdf and ax as instance variables to reuse them in other methods
        self.gdf = gdf
        self.ax = ax
        
        # Initially drawing the canvas
        self.canvas.draw()
        
    def setup_left_frame(self, left_frame):
        headline_label = tk.Label(left_frame, text="User Assignment", font=("Helvetica", 16))
        headline_label.grid(row=0, column=0, columnspan=3, pady=10)
        # Add your other widget setup here, similar to how you've set up in your provided code
        
        # Example:
        tk.Label(left_frame, text="Station").grid(row=1, column=0, sticky=tk.W)
        # Continue adding your form elements here as in your provided code
        
    def fetch_station_coordinates(self, station_name):
        con, cursor = get_database_connection()  # Assuming this function returns a connection and cursor
        if con and cursor:
            try:
                query = "SELECT lat, lon FROM station_coordinates WHERE station = %s"
                cursor.execute(query, (station_name,))
                result = cursor.fetchone()
                return result if result else (None, None)
            except mysql.Error as err:
                print(f"Error fetching station coordinates: {err}")
            finally:
                con.close()
        return None, None


    def save_changes(self):
        selected_indices = self.station_listbox.curselection()
        selected_stations = [self.station_listbox.get(i) for i in selected_indices]
        dbkey = self.dbkey_var.get()
        data_type = self.data_type_var.get()
        eff_date = self.eff_date_entry.get()
        username = self.username_var.get()
        qa_interval = self.qa_interval_entry.get()
        report_group = self.report_group_entry.get()
        budget_code = self.budget_code_entry.get()
        mandate = self.mandate_entry.get()
        ee_grade = self.ee_grade_entry.get()
        hrs_per_year = self.hrs_per_year_entry.get()
        customer_poc = self.customer_poc_entry.get()
        comments = self.comments_text.get("1.0", tk.END).strip()
        general_info_notes = self.general_info_text.get("1.0", tk.END).strip()
        task = self.task_entry.get()
        deadline = self.deadline_entry.get()

        # Check if the required fields are filled
        if not selected_stations or any(len(value.strip()) == 0 for value in [dbkey, data_type, eff_date, username, budget_code, customer_poc, task, deadline]):
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                con = mysql.connect(host="localhost", user="root", password="", database="stationandusermain")
                cursor = con.cursor()
                for station in selected_stations:
                    cursor.execute("INSERT INTO insertalldata VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                                (station, dbkey, data_type, eff_date, username, qa_interval, report_group, budget_code, mandate, ee_grade, hrs_per_year, customer_poc, comments, general_info_notes, task, deadline))
                con.commit()
                messagebox.showinfo("Successful", "Data Inserted Successfully!")
            except mysql.Error as err:
                messagebox.showerror("Database Error", f"An error occurred: {err}")
            finally:
                if con.is_connected():
                    con.close()

                   
if __name__ == "__main__":
    app = StationUserMaintenance()
    app.mainloop()
