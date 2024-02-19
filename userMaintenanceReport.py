import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UserMaintenanceReport(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QA Tool : User Maintenance Report")
        self.geometry("1150x880")
        img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
        self.iconphoto(False, img)

        # Create a frame
        frame = ttk.Frame(self, padding=10, borderwidth=1.5, relief="solid")
        frame.pack(fill=tk.BOTH, expand=True)

        # Heading
        heading_label = ttk.Label(frame, text="USER MAINTENANCE REPORT", font=('Helvetica', 16, 'bold'))
        heading_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Labels
        ttk.Label(frame, text="Select Station:").grid(row=1, column=0, sticky=tk.E)

        # Option menu for selecting station
        self.station_var = tk.StringVar()
        stations = ["G342A_C", "OtherStation1", "OtherStation2"]
        station_menu = ttk.Combobox(frame, textvariable=self.station_var, values=stations, state="readonly")
        station_menu.grid(row=1, column=1, padx=5, pady=5)
        station_menu.bind("<<ComboboxSelected>>", self.show_notes)

        # Variable notes
        self.notes_var = tk.StringVar()
        ttk.Label(frame, text="Notes:").grid(row=2, column=0, sticky=tk.E)
        notes_label = ttk.Label(frame, textvariable=self.notes_var, wraplength=400, justify=tk.LEFT, borderwidth=1.5, relief="solid")
        notes_label.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        # Data display in tabular form
        ttk.Label(frame, text="Data:").grid(row=3, column=0, sticky=tk.E)
        self.data_tree = ttk.Treeview(frame, columns=("Property", "Value"), show="headings", height=5)
        self.data_tree.heading("Property", text="Property")
        self.data_tree.heading("Value", text="Value")
        self.data_tree.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # Bar plot
        # ttk.Label(frame, text="Bar Plot:").grid(row=4, column=0, sticky=tk.E)
        self.bar_plot_frame = ttk.Frame(frame, borderwidth=1.5, relief="solid")
        self.bar_plot_frame.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

    def show_notes(self, event):
        # Sample data
        data = {
            "G342A_C": {"EFF_date": "15-jan-00", "Staff_name": "John", "Comment": "Some comment for G342A_C"},
            "OtherStation1": {"EFF_date": "20-feb-01", "Staff_name": "Jane", "Comment": "Comment for OtherStation1"},
            "OtherStation2": {"EFF_date": "10-mar-02", "Staff_name": "Bob", "Comment": "Another comment for OtherStation2"}
        }

        selected_station = self.station_var.get()

        if selected_station in data:
            notes = f"EFF_date: {data[selected_station]['EFF_date']}\n"
            notes += f"Staff_name: {data[selected_station]['Staff_name']}\n"
            notes += f"Comment: {data[selected_station]['Comment']}"
            self.notes_var.set(notes)

            # Display data in the Treeview widget
            self.display_data_table(data[selected_station])

            # Create a smaller and more professional bar plot
            self.create_bar_plot(data[selected_station])

        else:
            messagebox.showwarning("Data Not Found", f"No data available for station {selected_station}.")
            self.notes_var.set("")
            self.clear_data_table()
            self.clear_bar_plot()

    def display_data_table(self, data):
        self.clear_data_table()
        for key, value in data.items():
            self.data_tree.insert("", tk.END, values=(key, value))

    def clear_data_table(self):
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)

    def create_bar_plot(self, data):
        fig, ax = plt.subplots(figsize=(8, 5))  # Adjust the figure size as needed
        labels = list(data.keys())
        values = list(data.values())
        ax.bar(labels, values, color='skyblue')  # Adjust bar color as needed
        ax.set_ylabel("Values")
        # ax.set_title("Bar Plot")  # Add a title to the plot

        canvas = FigureCanvasTkAgg(fig, master=self.bar_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear_bar_plot(self):
        for widget in self.bar_plot_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = UserMaintenanceReport()
    app.mainloop()