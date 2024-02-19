from logging import root
import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from random import choice
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from random import choice
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import tkinter as tk
from matplotlib.dates import DateFormatter, AutoDateLocator


FILE_LOCATION = "./csv files"
BUTTON_FONT = ("Arial", 13, "bold")
LABEL_FONT = ("Arial", 20, "bold")
USER_FONT = ("Arial", 14, "bold")
INFO_FONT = ("Arial", 12, "bold")
SMALL_FONT = ("Arial", 12, "normal")
COLORS = ['green', 'red', 'purple', 'brown', 'blue']

class Visualization:
    def __init__(self, window):
        self.window = window
        self.window.title("Data Assessment")
        self.window.geometry("1358x695")
        # self.window.state("zoomed")
        # self.window.config(bg="pale goldenrod")
        # extra variables:
        self.df = pd.DataFrame()
        self.bar_x_label = StringVar()
        self.bar_y_label = StringVar()
        self.scatter_x_name = StringVar()
        self.scatter_y_name = StringVar()
        self.pie_value_name = StringVar()
        self.pie_group_name = StringVar()
        self.line_name = StringVar()
        
        # ================================ TOP FRAME ================================ #
        self.top_frame = Frame(self.window, bg="light sea green", relief=RIDGE)
        self.top_frame.place(x=2, y=0, width=1363, height=40)

        self.build_chart = Label(self.top_frame, text="Data Assessment", font=LABEL_FONT,
                                 fg="khaki", bg="light sea green")
        self.build_chart.place(x=500, y=2)

        # =================================== LEFT FRAME ================================ #
        self.left_frame = Frame(self.window, bg="white smoke", relief=RIDGE, bd=1)
        self.left_frame.place(x=2, y=45, width=320, height=645)
        
        # Open CSV File button now placed at the top
        self.open_file_button = Button(self.left_frame, text="Open CSV File", justify="center",
                                       font=INFO_FONT, bg="honeydew", cursor="hand2", bd=0,
                                       command=self.file_open)
        self.open_file_button.place(x=45, y=10)  # Adjust y position to ensure it's above
        
        # Table to display CSV data will be initialized here but populated in file_open
        self.my_table = ttk.Treeview(self.left_frame)
        # scroll_x_label = ttk.Scrollbar(self.left_frame, orient=HORIZONTAL, command=self.my_table.xview)
        # scroll_y_label = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.my_table.yview)
        # scroll_x_label.pack(side=BOTTOM, fill=X)
        # scroll_y_label.pack(side=RIGHT, fill=Y)
        self.my_table.place(x=5, y=50, width=310, height=590)
        
        # ================================ RIGHT FRAME ================================ #
        self.right_frame = Frame(self.window, bg="white smoke", relief=RIDGE, bd=1)
        self.right_frame.place(x=330, y=45, width=1025, height=645)

        # Button to show outliers
        self.show_outliers_button = Button(self.right_frame, text="Outliers", font=INFO_FONT,
                                   bg="honeydew", cursor="hand2", bd=2,  # Increased border width
                                   command=self.show_outliers)
        self.show_outliers_button.place(x=10, y=10)
        
        self.show_anomalies_button = Button(self.right_frame, text="Anomalies", font=INFO_FONT,
                                            bg="honeydew", cursor="hand2", bd=2,  # Increased border width
                                            command=self.show_anomalies)
        self.show_anomalies_button.place(x=120, y=10)

        # Frame to display outliers plot
        self.outliers_frame = Frame(self.right_frame, bg="white")
        self.outliers_frame.place(x=10, y=50, width=1000, height=585)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="silver", foreground="black", rowheight=25, fieldbackground="silver")
        style.map("Treeview", background=[("selected", "medium sea green")])
        style.configure("Treeview.Heading", background="light steel blue", font=("Arial", 10, "bold"))

        self.my_table = ttk.Treeview(self.left_frame)

        scroll_x_label = ttk.Scrollbar(self.left_frame, orient=HORIZONTAL, command=self.my_table.xview)
        scroll_y_label = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.my_table.yview)
        scroll_x_label.pack(side=BOTTOM, fill=X)
        scroll_y_label.pack(side=RIGHT, fill=Y)

        # add menu bar:
        my_menu = Menu(self.window)
        self.window.config(menu=my_menu)
        self.file_menu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="Available SpreadSheets", menu=self.file_menu)
        self.file_menu.add_command(label="open file", command=self.file_open)

    # ================================= FUNCTIONALITY =============================== #
    def file_open(self):
        file_name = filedialog.askopenfilename(
            initialdir=FILE_LOCATION,
            title="Open A File",
            filetypes=(("csv files", "*.csv"), ("All Files", "*.*"))
        )
        if file_name:
            try:
                file_name = f"{file_name}"
                self.df = pd.read_csv(file_name)
            except ValueError:
                self.error_info.config(text="file can not be opened!")
            except FileNotFoundError:
                self.error_info.config(text="file can not be found!")

        # clean existing data:
        self.clear_table_data()
        # from csv into dataframe:
        self.my_table["column"] = list(self.df.columns)
        self.my_table["show"] = "headings"
        for column in self.my_table["column"]:
            self.my_table.heading(column, text=column)
        # resize columns:
        for column_name in self.my_table["column"]:
            self.my_table.column(column_name, width=60)
        # fill rows with data:
        df_rows_old = self.df.to_numpy()
        df_rows_refreshed = [list(item) for item in df_rows_old]
        for row in df_rows_refreshed:
            self.my_table.insert("", "end", values=row)
        self.my_table.place(x=5, y=5, width=310, height=630)

    def clear_table_data(self):
        self.my_table.delete(*self.my_table.get_children())
        

    # ================================ FILL COMBOBOX METHODS ============================= #
    def fill_bar_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == 'object':
                x_labels.append(column)
            elif self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                y_labels.append(column)
        self.x_box["values"] = tuple(x_labels)
        self.x_box.current(0)
        self.y_box["values"] = tuple(y_labels)
        self.y_box.current(0)

    def show_spreadsheet_button_click(self):
        file_name = filedialog.askopenfilename(
            initialdir=FILE_LOCATION,
            title="Open A File",
            filetypes=(("csv files", "*.csv"), ("All Files", "*.*"))
        )
        if file_name:
            try:
                file_name = f"{file_name}"
                self.df = pd.read_csv(file_name)
            except ValueError:
                self.error_info.config(text="file can not be opened!")
            except FileNotFoundError:
                self.error_info.config(text="file can not be found!")
        
    def show_outliers(self):
        if self.df.empty:
            messagebox.showinfo("Information", "Please load a dataset first.")
            return

        if 'Value' not in self.df.columns:
            messagebox.showinfo("Error", "The dataset must contain a 'Value' column.")
            return
        
        # Clearing the frame before plotting a new figure
        for widget in self.outliers_frame.winfo_children():
            widget.destroy()
    
        # Focusing solely on the 'Value' column for outlier detection
        fig, ax = plt.subplots()
        sns.boxplot(y=self.df['Value'], ax=ax, color='lightblue')
        ax.set_title("Outliers")
        
        # Detecting outliers based on IQR
        Q1 = self.df['Value'].quantile(0.25)
        Q3 = self.df['Value'].quantile(0.75)
        IQR = Q3 - Q1
        threshold_upper = Q3 + 1.5 * IQR
        threshold_lower = Q1 - 1.5 * IQR
        
        # Identifying outliers
        outliers = self.df[(self.df['Value'] > threshold_upper) | (self.df['Value'] < threshold_lower)]
        
        # Highlighting outliers on the plot and annotating with detailed information
        for index, outlier in outliers.iterrows():
            ax.plot(0, outlier['Value'], 'ro')  # Plotting red dots for outliers
            ax.annotate(f"{outlier['Value']}", (0, outlier['Value']), textcoords="offset points", xytext=(0,10), ha='center')
        
        # Displaying the plot in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.outliers_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill='both')
        
        # Clearing the figure to free memory
        plt.close(fig)

            
    def identify_outliers(self, data):
        # Use IQR method to identify outliers
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = data[(data < lower_bound) | (data > upper_bound)]
        return outliers
    
    def show_anomalies(self):
        if self.df.empty:
            messagebox.showwarning("Warning", "Please open a CSV file first.")
            return

        for widget in self.outliers_frame.winfo_children():
            widget.destroy()

        # Assuming 'x_column' is your date column and it might not be in datetime format
        if len(self.df.columns) < 4:
            messagebox.showwarning("Warning", "At least 4 columns are required for anomalies (x, y, and two others).")
            return

         # Assuming 'x_column' is your date column and it might not be in datetime format
  
        # Check if there are at least 4 columns for x and y axis
        if len(self.df.columns) < 4:
            messagebox.showwarning("Warning", "At least 4 columns are required for anomalies (x, y, and two others).")
            return

        # Select the 3rd and 4th columns for x and y axis
        # Assuming 'x_column' is your date column and it might not be in datetime format
        x_column = self.df.columns[1]  # Example, adjust as necessary
        self.df[x_column] = pd.to_datetime(self.df[x_column])  # Convert to datetime if not already
        y_column = self.df.columns[2]
  # Convert to datetime if not already
    
        y_column = self.df.columns[2]

        # Identify anomalies
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed

        ax.plot(self.df[x_column], self.df[y_column], label='Normal Data', color='blue', linewidth=2)
        anomalies = self.identify_anomalies(self.df[y_column])
        ax.scatter(self.df.loc[anomalies.index, x_column], anomalies, color='red', label='Anomalies')
    
        ax.set_title("Anomalies Detection")
        ax.set_xlabel("Date")
        ax.set_ylabel(y_column)
        ax.legend()

        # Save the plot to a temporary file
        ax.xaxis.set_major_locator(AutoDateLocator())
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        plt.gcf().autofmt_xdate()  # Rotation
    
        # Display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.outliers_frame)  # Adjust 'master' as necessary
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
    
        plt.close(fig)
        
    def identify_anomalies(self, data):
        # Identify anomalies based on a simple threshold (you can customize this logic)
        threshold = 2.5
        anomalies = data[data > threshold]
        return anomalies

def launch_program():
        app = Tk()
        Visualization(app)
        app.mainloop()

if __name__ == "__main__":
    launch_program()