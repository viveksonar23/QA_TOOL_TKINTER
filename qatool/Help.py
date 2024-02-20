import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from PIL.ImageTk import PhotoImage
from fpdf import FPDF
from pathlib import Path

class HelpPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QA Tool : Help")
        self.geometry("1132x611+300+100")

        frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Help content
        help_content = {
            "Contact Numbers": "Emergency: 911\nSupport: 123-456-7890",
            "Email": "support@example.com",
            "Common Questions": "1. How to reset my password?\n2. Where can we see the water data?",
            "About any issue": "This page provides assistance for various queries.",
        }

        # Display help content
        for i, (label, content) in enumerate(help_content.items()):
            ttk.Label(frame, text=label, font=('Arial', 14, 'bold')).grid(row=i, column=0, sticky=tk.W)
            ttk.Label(frame, text=content, wraplength=300).grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)

        # Button to add screenshots
        ttk.Button(frame, text="How to Create the User?", command=self.add_screenshots).grid(row=len(help_content), column=0, pady=10, sticky=tk.W)

    def add_screenshots(self):
        # Create a new window for user guidance with labels and images
        screenshot_window = tk.Toplevel(self)
        screenshot_window.title("User Creation Guide")
        screenshot_window.geometry("1132x780+300+100")

        # Example: Replace this with the actual path to your screenshots
        image_paths = ["/Users/viveksonar/Desktop/FinalData/admincontrol.png", "/Users/viveksonar/Desktop/FinalData/usercreation.png"]

        # Display labels and images in the new window
        for i, image_path in enumerate(image_paths):
            # Load image and resize it if necessary
            img = Image.open(image_path)
            img = img.resize((300, 200))  # Use Image.ANTIALIAS directly
            img = PhotoImage(img)

            # Create a label to display the image
            image_label = ttk.Label(screenshot_window, image=img)
            image_label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)

            # Keep a reference to the image to prevent it from being garbage collected
            image_label.image = img

        # Information label
        information_label_text = (
            "This section, titled 'Administration Control,' is specifically designated for administrators. In this module, administrators have the capability to create new users. The user creation process involves inputting both the first and last names into designated entry boxes. After entering this information, administrators can proceed by clicking the 'User Creation' button.\n\n"
            "It is essential to note that the data entered during user creation is securely stored in a SQL database, ensuring data integrity and accessibility as needed.\n\n"
            "Additionally, administrators are granted access to a specific password, initially provided by the developer. For security reasons, administrators are encouraged to contact the developer to obtain the password. Once obtained, administrators have the option to change the password for heightened security and user management. This feature ensures that only authorized personnel can access and modify critical administrative settings."
        )
        ttk.Label(screenshot_window, text=information_label_text, wraplength=600).grid(row=len(image_paths), column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Button to download PDF
        ttk.Button(screenshot_window, text="Download PDF", command=lambda: self.download_pdf(image_paths)).grid(row=len(image_paths) + 1, column=0, columnspan=2, pady=10, sticky=tk.W)

    def download_pdf(self, image_paths):
        pdf_file_path = "/Users/viveksonar/Downloads/help_documentation.pdf"
        information_label_text = (
            "This section, titled 'Administration Control,' is specifically designated for administrators. In this module, administrators have the capability to create new users. The user creation process involves inputting both the first and last names into designated entry boxes. After entering this information, administrators can proceed by clicking the 'User Creation' button.\n\n"
            "It is essential to note that the data entered during user creation is securely stored in a SQL database, ensuring data integrity and accessibility as needed.\n\n"
            "Additionally, administrators are granted access to a specific password, initially provided by the developer. For security reasons, administrators are encouraged to contact the developer to obtain the password. Once obtained, administrators have the option to change the password for heightened security and user management. This feature ensures that only authorized personnel can access and modify critical administrative settings."
        )
        # Create PDF with help content and images
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=14)

        # Add text information to PDF
        pdf.multi_cell(0, 10, information_label_text)

        # Add images to PDF
        for image_path in image_paths:
            pdf.ln(10)  # Add some space between text and image
            pdf.image(image_path, x=pdf.get_x(), w=pdf.w - 20)  # Adjust width to fit the page

        pdf.output("/Users/viveksonar/Downloads/help_documentation.pdf")
        messagebox.showinfo("Download Successful", f"The help documentation has been successfully downloaded to {pdf_file_path}.\n\nYou can access it from the Downloads folder.")

    def open_image(self, image_path):
        # Open the image using the default image viewer
        image_path = Path(image_path)
        image_path.absolute().startfile()

if __name__ == "__main__":
    app = HelpPage()
    app.mainloop()