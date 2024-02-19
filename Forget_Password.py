import subprocess
import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk
import mysql.connector as mysql

class PasswordResetApp:
    def __init__(self, root):
        self.root = root
        self.root.title('QA Tool : Forgot Password')
        self.root.geometry('1132x611+300+100')
        self.root.configure(bg="#fff")
        self.root.resizable(True, True)
        img = PhotoImage(file='/Users/viveksonar/Desktop/project_research/iconssss.png')
        self.root.iconphoto(False, img)
        self.create_password_window = None  # Initialize the reference for the Toplevel window
        self.init_ui()

    def show_message_box(self, title, message, delay=1500):
        messagebox.showinfo(title, message)
        self.root.update()
        self.root.after(delay, self.root.focus_force)

    def get_database_connection(self):
        try:
            con = mysql.connect(host="localhost", user="root", password="", database="aut")
            cursor = con.cursor()
            return con, cursor
        except mysql.Error as err:
            print(f"Error: {err}")
            return None, None

    def validate_user(self, username, security_question, security_answer):
        con, cursor = self.get_database_connection()
        if con and cursor:
            try:
                query = "SELECT * FROM auth WHERE username = %s AND security_question = %s AND security_answer = %s"
                cursor.execute(query, (username, security_question, security_answer))
                result = cursor.fetchone()
                return result is not None
            except mysql.Error as err:
                print(f"Error: {err}")
            finally:
                con.close()
        return False

    def update_password_for_username(self, username, new_password):
        con, cursor = self.get_database_connection()
        if con and cursor:
            try:
                update_query = "UPDATE auth SET password = %s WHERE username = %s"
                cursor.execute(update_query, (new_password, username))
                con.commit()
                print(f"Password for username {username} updated successfully.")
            except mysql.Error as e:
                print(f"Error: {e}")
            finally:
                con.close()

    def set_new_password(self, username):
        self.root.withdraw()
        
        # Create a new Toplevel window
        self.create_password_window = tk.Toplevel(self.root)
        self.create_password_window.title("Set New Password")
        self.create_password_window.geometry('1132x611+300+100')
        
        # Create and place the frame within the Toplevel window
        set_password_frame = tk.Frame(self.create_password_window, width=400, height=200, bd=5, relief='solid', borderwidth=1)
        set_password_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Create Password label and entry field
        label_createpassword = tk.Label(set_password_frame, text='Create Password', font=('Microsoft YaHei UI Light', 15))
        label_createpassword.grid(row=0, column=0, pady=5, padx=5)
        createpassword_entry = tk.Entry(set_password_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid")
        createpassword_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Confirm Password label and entry field
        label_confirmpassword = tk.Label(set_password_frame, text='Confirm Password', font=('Microsoft YaHei UI Light', 15))
        label_confirmpassword.grid(row=1, column=0, pady=5, padx=5)
        confirmpassword_entry = tk.Entry(set_password_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid")
        confirmpassword_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Function to save the new password
        def save_new_password():
            new_password = createpassword_entry.get()
            confirm_new_password = confirmpassword_entry.get()
            
            if new_password and confirm_new_password and new_password == confirm_new_password:
                self.update_password_for_username(username, new_password)
                self.show_message_box("Password Updated", "Your password has been updated successfully.")
                self.create_password_window.destroy()  # Close the set new password window
                self.root.destroy()  # Close the forget password window
                self.open_login_window()  # Close the window upon successful update
            else:
                self.show_message_box("Error", "Passwords do not match. Please try again.")
        
        # Set Password button
        set_password_button = ttk.Button(set_password_frame, text="Set Password", command=save_new_password)
        set_password_button.grid(row=2, column=1, columnspan=2, pady=10)

    def init_ui(self):
        self.img = tk.PhotoImage(file='/Users/viveksonar/Desktop/project_research/zoomimagepeopr.png')
        tk.Label(self.root, image=self.img, bg='white').place(x=0, y=0, relwidth=1, relheight=1)

        # Frame for the Forgot Password section
        self.forget_password_frame = tk.Frame(self.root, width=500, height=300, bd=5, relief='solid', borderwidth=1)
        self.forget_password_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label_username = tk.Label(self.forget_password_frame, text='Username:', font=('Microsoft YaHei UI Light', 15))
        self.label_username.grid(row=0, column=0, pady=5, padx=5)

        self.username_entry = tk.Entry(self.forget_password_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid")
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        self.label_security_question = tk.Label(self.forget_password_frame, text='Select Security Question:', font=('Microsoft YaHei UI Light', 15))
        self.label_security_question.grid(row=1, column=0, pady=5, padx=5)

        self.security_questions = ["What is the name of your first car?", "Which Elementary school did you attend?"]
        self.security_question_combobox = ttk.Combobox(self.forget_password_frame, values=self.security_questions, width=28, font=('Microsoft YaHei UI Light', 15), state="readonly")
        self.security_question_combobox.grid(row=1, column=1, pady=5, padx=5)
        self.security_question_combobox.current(0)  # Optional: set default value

        self.label_answer = tk.Label(self.forget_password_frame, text='Enter Security Answer:', font=('Microsoft YaHei UI Light', 15))
        self.label_answer.grid(row=2, column=0, pady=5, padx=5)

        self.answer_entry = tk.Entry(self.forget_password_frame, width=30, font=('Microsoft YaHei UI Light', 15), bd=1, relief="solid")
        self.answer_entry.grid(row=2, column=1, pady=5, padx=5)

        self.submit_button = ttk.Button(self.forget_password_frame, text="Submit", command=self.check_answer)
        self.submit_button.grid(row=3, column=1, pady=10)
        
    def open_login_window(self):
        subprocess.Popen(["python3", "Login.py"], shell=False)

    def check_answer(self):
        username = self.username_entry.get()
        security_question = self.security_question_combobox.get()
        security_answer = self.answer_entry.get()

        if not all([username, security_question, security_answer]):
            self.show_message_box("Error", "Please fill in all fields.")
            return

        if self.validate_user(username, security_question, security_answer):
            self.show_message_box("Valid User", "You can set a new password now.")
            self.set_new_password(username)
        else:
            self.show_message_box("Error", "Invalid Username or Security Question/Answer.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordResetApp(root)
    root.mainloop()
