import tkinter as tk
from tkinter import PhotoImage, ttk

class AboutPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QA Tool : About Water Data Project")
        self.geometry("1132x611+300+100")
        img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
        self.iconphoto(False, img)

        frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # About content
        about_content = {
            "Project Name": "HDET Water Data Project",
            "Description": "This project focuses on collecting and analyzing water-related data for environmental research.",
            "Features": [
                "Real-time water quality monitoring",
                "Data visualization and analysis tools",
                "User-friendly interface",
                "Secure user authentication",
                "Collaboration and sharing capabilities",
            ],
            "More Information": "For more details and updates, visit our website:",
            "Website Link": "https://example.com/water_data_project",
        }

        # Display about content
        for i, (label, content) in enumerate(about_content.items()):
            if label == "Features":
                ttk.Label(frame, text=f"{label}:", font=('Arial', 14, 'bold')).grid(row=i, column=0, sticky=tk.W)
                for j, feature in enumerate(content, start=1):
                    ttk.Label(frame, text=f"   {j}. {feature}", wraplength=300).grid(row=i+j, column=0, columnspan=2, padx=10, pady=2, sticky=tk.W)
            elif label == "More Information":
                ttk.Label(frame, text=content, font=('Arial', 14, 'bold')).grid(row=i, column=0, columnspan=2, sticky=tk.W)
            else:
                ttk.Label(frame, text=f"{label}: {content}", font=('Arial', 14, 'bold')).grid(row=i, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Link to the website
        website_link = ttk.Label(frame, text=about_content["Website Link"], cursor="hand2", foreground="blue")
        website_link.grid(row=len(about_content), column=0, columnspan=2, pady=10)
        website_link.bind("<Button-1>", self.open_website)

    def open_website(self, event):
        import webbrowser
        webbrowser.open("https://example.com/water_data_project")

if __name__ == "__main__":
    app = AboutPage()
    app.mainloop()