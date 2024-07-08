import tkinter as tk
from tkinter import messagebox
import hashlib,mysql.connector,login,re,secrets,string
from connector import mydb, cursor
from utils import fetch_and_display_image

class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mydb = mydb
        self.canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=1280,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0, 214, 209)
        self.image_image_2 = fetch_and_display_image(self,"https://media.tenor.com/bjLh2iYjW_cAAAAM/kau.gif", 1180.0, 107, 180, 209)

        self.canvas.create_text(
            496.0,
            85.0,
            anchor="nw",
            text="Registering Form",
            fill="#000000",
            font=("Inter", 36 * -1)
        )

        self.name_entry = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.name_entry.place(
            x=477.0,
            y=219.0,
            width=325.0,
            height=45.0
        )

        self.email_entry = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.email_entry.place(
            x=477.0,
            y=307.0,
            width=325.0,
            height=45.0
        )

        self.password_entry = tk.Entry(self, bd=0, bg="#F8F8F8", show="*", fg="#000716", highlightthickness=0)
        self.password_entry.place(
            x=477.0,
            y=394.0,
            width=325.0,
            height=45.0
        )
        
        login_btn = tk.Button(self, text="Log In", font=20, borderwidth=0, highlightthickness=0,
                              command=lambda: controller.show_frame(login.Login), relief="flat")
        login_btn.place(
            x=642.0,
            y=450,
            width=160.0,
            height=50
        )

        register_btn = tk.Button(self, text="Create Account", font=20, borderwidth=0, highlightthickness=0,
                                 command=self.validate_and_register, relief="flat")
        register_btn.place(
            x=477.0,
            y=450,
            width=160.0,
            height=50
        )
        
        self.canvas.create_text(
            477.0,
            192.0,
            anchor="nw",
            text="Name",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            477.0,
            277.0,
            anchor="nw",
            text="Email Address",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            477.0,
            365.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            477.0,
            510.0,
            anchor="nw",
            text="*By creating account, you state that you \nhave read and understood the terms.",
            fill="#FF0000",
            font=("Inter Light", 16 * -1)
        )

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def clear_registration_fields(self):
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')


    def validate_and_register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Password policy regular expression pattern
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,24}$"
        
        # Email pattern to check for .com or .org at the end
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org)$"
        
        if not name or not email or not password:
            tk.messagebox.showerror("Error", "All fields must be filled.")
            return

        if not re.match(email_pattern, email):
            tk.messagebox.showerror("Error", "Invalid email address. Email must end with .com or .org.")
            return
        
        if not re.match(password_pattern, password):
            tk.messagebox.showerror("Error", "Password must be between 8-24 characters and contain at least one lowercase letter, one uppercase letter, one digit, and one special symbol (!@#$%^&*()_+).")
            return

        hashed_password = self.hash_password(password)

        cursor = mydb.cursor()
        sql = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        val = (email, name, hashed_password)
        
        try:
            cursor.execute(sql, val)
            mydb.commit()
            tk.messagebox.showinfo("Success", "Registration successful!")
            self.clear_registration_fields()
            self.controller.show_frame(login.Login)
        except mysql.connector.Error as err:
            tk.messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
