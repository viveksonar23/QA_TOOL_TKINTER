import os
import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import simpledialog
from tkinter import messagebox
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

from matplotlib import pyplot as plt


def show_message_box(title, message, delay=1500):
    messagebox.showinfo(title, message)
    root.update()
    root.after(delay, root.focus_force)

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QA Tool : Task Manager")
        self.root.geometry("1132x611+300+100")
        img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
        self.root.iconphoto(False, img)

        self.tasks = [
            {"id": 1, "title": "Task 1", "status": "Not Started", "assigned_to": "Vivek"},
            {"id": 2, "title": "Task 2", "status": "In Progress", "assigned_to": "Vivek2"},
            {"id": 3, "title": "Task 3", "status": "Completed", "assigned_to": "Vishal"},
            {"id": 4, "title": "Task 4", "status": "Not Started", "assigned_to": "Vishal2"},
            {"id": 5, "title": "Task 5", "status": "Not Started", "assigned_to": "Rishabh"},
            {"id": 6, "title": "Task 6", "status": "Not Started", "assigned_to": "Rishabh2"},
            {"id": 7, "title": "Task 7", "status": "Not Started", "assigned_to": "Sonar"},
        ]
        self.user_statuses = self.calculate_user_statuses()

        # Add a border around the frame
        self.user_status_frame = ttk.Frame(self.root, borderwidth=1.5, relief="solid")
        self.user_status_frame.pack(pady=10)

        self.user_status_label = ttk.Label(self.user_status_frame, text="User Status:", font=('Arial', 16, 'bold'))
        self.user_status_label.grid(row=0, column=0, columnspan=5)

        self.user_status_tree = ttk.Treeview(self.user_status_frame, columns=("In Progress", "Completed", "Not Started"))
        self.user_status_tree.grid(row=1, column=0, columnspan=5, sticky="nsew")

        # Add column lines between columns
        for col_index, col in enumerate(["In Progress", "Completed"]):
            self.user_status_tree.column(col, width=100, anchor="center")
            self.user_status_tree.heading(col, text=col)
            self.user_status_frame.grid_columnconfigure(col_index, weight=1)

        self.user_status_tree.heading("Not Started", text="Not Started")

        self.update_user_status_tree()

        # Add a border around the frame
        self.task_list_frame = ttk.Frame(self.root, borderwidth=1.5, relief="solid")
        self.task_list_frame.pack(pady=10)

        self.task_list_label = ttk.Label(self.task_list_frame, text="Task List:", font=('Arial', 16, 'bold'))
        self.task_list_label.grid(row=0, column=0, columnspan=6)

        self.task_tree = ttk.Treeview(self.task_list_frame, columns=("ID", "Title", "Status", "Assigned To", "Color"))
        self.task_tree.grid(row=1, column=0, columnspan=6, sticky="nsew")

        # Add column lines between columns
        for col_index, col in enumerate(["ID", "Title", "Status", "Assigned To"]):
            self.task_tree.column(col, width=100, anchor="center")
            self.task_tree.heading(col, text=col)
            self.task_list_frame.grid_columnconfigure(col_index, weight=1)

        self.update_task_tree()

        self.start_button = ttk.Button(self.task_list_frame, text="Start", command=self.start_task)
        self.start_button.grid(row=2, column=1, padx=5)

        self.complete_button = ttk.Button(self.task_list_frame, text="Complete", command=self.complete_task)
        self.complete_button.grid(row=2, column=2, padx=5)

        self.user_status_tree.tag_configure('In Progress', background='yellow')
        self.user_status_tree.tag_configure('Completed', background='green')

        self.report_button = ttk.Button(self.task_list_frame, text="Create Report", command=self.create_report)
        self.report_button.grid(row=2, column=3, padx=5)

        # Add row lines between rows
        for i in range(1, 6):
            self.user_status_tree.insert("", "end", values=("","",""))
            self.task_tree.insert("", "end", values=("","","","",""))

    def create_report(self):
        default_download_folder = os.path.expanduser("~" + os.sep + "Downloads")
        file_name = simpledialog.askstring("Report", "Enter file name for the report:", initialvalue="TaskReport.pdf")

        if file_name:
            file_path = os.path.join(default_download_folder, file_name)
            try:
                # Create a PDF report
                doc = SimpleDocTemplate(file_path, pagesize=letter)
                styles = getSampleStyleSheet()
                content = []

                # Add title to the report
                content.append(Paragraph(f"<u>Task Manager Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</u>", styles['Title']))

                # Add task status table
                status_data = [["User", "In Progress", "Completed", "Not Started"]]
                for user, status in self.user_statuses.items():
                    status_data.append([user, status["In Progress"], status["Completed"], status["Not Started"]])

                status_table = Table(status_data, colWidths=[100, 80, 80, 80])
                status_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))
                content.append(Paragraph("<br/><b>Task Status:</b>", styles['Heading1']))
                content.append(status_table)

                # Add detailed user information table
                user_info_data = [["User", "Task ID", "Title", "Status"]]
                for user in self.user_statuses:
                    for task in self.tasks:
                        if task["assigned_to"] == user:
                            user_info_data.append([user, task["id"], task["title"], task["status"]])

                user_info_data = [["User", "Task ID", "Title", "Status"]]
                for user in self.user_statuses:
                    for task in self.tasks:
                        if task["assigned_to"] == user:
                            user_info_data.append([user, task["id"], task["title"], task["status"]])

                user_info_table = Table(user_info_data, colWidths=[100, 50, 200, 80])
                user_info_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))
                content.append(Paragraph("<br/><b>Detailed User Information:</b>", styles['Heading1']))
                content.append(user_info_table)

# Add pie chart to the report
                # pie_chart_path = self.generate_pie_chart()

                # # Now, add the pie chart below the detailed user information
                # content.append(Paragraph("<br/><b>Task Status Distribution:</b>", styles['Heading1']))
                # content.append(Paragraph(f"<img src='{pie_chart_path}' width='400' height='300'/><br/>", styles['Normal']))

                # # Save the PDF report
                doc.build(content)

                show_message_box("Report Created", f"Report successfully created and saved as {file_path}")
            except Exception as e:
                show_message_box("Error", f"An error occurred: {str(e)}")
        else:
            show_message_box("Report Cancelled", "Report creation cancelled by user")


    def generate_pie_chart(self):
        labels = ['In Progress', 'Completed', 'Not Started']
        sizes = [sum(status['In Progress'] for status in self.user_statuses.values()),
                 sum(status['Completed'] for status in self.user_statuses.values()),
                 sum(status['Not Started'] for status in self.user_statuses.values())]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['yellow', 'green', 'black'])
        ax.axis('equal')

        pie_chart_path = os.path.expanduser("~" + os.sep + "Downloads" + os.sep + "pie_chart.png")
        fig.savefig(pie_chart_path)
        plt.close(fig)
        return pie_chart_path

    # def display_pie_chart(self):
    #     labels = ['In Progress', 'Completed', 'Not Started']
    #     sizes = [sum(status['In Progress'] for status in self.user_statuses.values()),
    #              sum(status['Completed'] for status in self.user_statuses.values()),
    #              sum(status['Not Started'] for status in self.user_statuses.values())]

    #     fig, ax = plt.subplots()
    #     ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['yellow', 'green', 'black'])
    #     ax.axis('equal')

    #     plt.title("Task Status Distribution")
    #     plt.show()

    def update_user_status_tree(self):
        for user, status in self.user_statuses.items():
            values = (status["In Progress"], status["Completed"], status["Not Started"])
            item = self.user_status_tree.insert("", "end", text=user, values=values)

            # Apply tags based on status for cell colors
            if status["In Progress"] > 0:
                self.user_status_tree.item(item, tags=('In Progress',))
            if status["Completed"] > 0:
                self.user_status_tree.item(item, tags=('Completed',))

    def calculate_user_statuses(self):
        user_statuses = {}
        for task in self.tasks:
            user = task["assigned_to"]
            if user not in user_statuses:
                user_statuses[user] = {"In Progress": 0, "Completed": 0, "Not Started": 0}
            user_statuses[user][task["status"]] += 1
        return user_statuses

    def update_task_tree(self):
        for task in self.tasks:
            values = (task["id"], task["title"], task["status"], task["assigned_to"], "")
            item = self.task_tree.insert("", "end", text="", values=values)

            # # Set color dot based on status
            # if task["status"] == "In Progress":
            #     self.task_tree.item(item, values=(task["id"], task["title"], task["status"], task["assigned_to"], "yellow"))
            # elif task["status"] == "Completed":
            #     self.task_tree.item(item, values=(task["id"], task["title"], task["status"], task["assigned_to"], "green"))
            # else:
            #     self.task_tree.item(item, values=(task["id"], task["title"], task["status"], task["assigned_to"], "black"))

    def start_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_id = int(self.task_tree.item(selected_item, "values")[0])
            for task in self.tasks:
                if task["id"] == task_id and task["status"] == "Not Started":
                    task["status"] = "In Progress"
                    self.update_ui()

    def complete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_id = int(self.task_tree.item(selected_item, "values")[0])
            for task in self.tasks:
                if task["id"] == task_id and task["status"] == "In Progress":
                    task["status"] = "Completed"
                    self.update_ui()

    def update_ui(self):
        self.user_statuses = self.calculate_user_statuses()
        self.user_status_tree.delete(*self.user_status_tree.get_children())
        self.update_user_status_tree()
        self.task_tree.delete(*self.task_tree.get_children())
        self.update_task_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
