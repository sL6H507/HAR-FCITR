import tkinter as tk
from tkinter import messagebox
import hashlib,mysql.connector,home,register,secrets,string
from datetime import datetime
from connector import mydb, cursor
from utils import fetch_and_display_image


class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mydb = mydb

        self.canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0, 214, 209)
        self.image_image_2 = fetch_and_display_image(self,"https://media.tenor.com/bjLh2iYjW_cAAAAM/kau.gif", 1180.0, 107, 180, 209)

        self.canvas.create_text(
            545.0,
            108.0,
            anchor="nw",
            text="Login Form",
            fill="#000000",
            font=("Inter", 36)
        )

        self.email_entry = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.email_entry.place(
            x=477.0,
            y=271.0,
            width=325.0,
            height=44.0
        )

        self.password_entry = tk.Entry(self, bd=0, show="*", bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.password_entry.place(
            x=477.0,
            y=356.0,
            width=325.0,
            height=44.0
        )

        login_btn = tk.Button(self, text="Log In", font=20, borderwidth=0, highlightthickness=0,
                              command=self.validate_and_login, relief="flat")
        login_btn.place(
            x=477.0,
            y=420,
            width=160.0,
            height=50
        )

        register_btn = tk.Button(self, text="Create Account", font=20, borderwidth=0, highlightthickness=0,
                                 command=lambda: controller.show_frame(register.Register), relief="flat")
        register_btn.place(
            x=642.0,
            y=420,
            width=160.0,
            height=50
        )

        self.canvas.create_text(
            477.0,
            242.0,
            anchor="nw",
            text="Email Address",
            fill="#000000",
            font=("Inter", 20)
        )

        self.canvas.create_text(
            477.0,
            327.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Inter", 20)
        )

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def clear_login_fields(self):
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def update_last_signed(self, email):
        cursor = self.mydb.cursor()
        sql = "UPDATE users SET lastsigned = %s WHERE email = %s"
        val = (datetime.now(), email)
        try:
            cursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating last signed: {err}")
        finally:
            cursor.close()

    def update_last_failed_signed(self, email):
        cursor = self.mydb.cursor()
        sql = "UPDATE users SET failedsign = %s WHERE email = %s"
        val = (datetime.now(), email)
        try:
            cursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating last signed: {err}")
        finally:
            cursor.close()

    def generate_session_id(self, length):
        characters = string.ascii_letters + string.digits
        session_id = ''.join(secrets.choice(characters) for _ in range(length))
        return session_id

    def validate_and_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        hashed_password = self.hash_password(password)
        
        cursor = self.mydb.cursor()
        sql = "SELECT password FROM users WHERE email = %s"
        val = (email,)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if hashed_password == stored_password:
                # Generate session ID for the user
                session_id = self.generate_session_id(length=64)
                
                # Update last signed in and set session ID in database
                self.update_last_signed(email)
                sql_update_session = "UPDATE users SET session_id = %s WHERE email = %s"
                val_update_session = (session_id, email)
                cursor.execute(sql_update_session, val_update_session)
                self.mydb.commit()
                
                messagebox.showinfo("Success", "Login successful!")
                self.clear_login_fields()
                
                # Set session ID in controller
                self.controller.set_session(session_id)
                
                # Show homepage frame with authentication
                self.controller.show_frame_with_auth(home.HomePage)
            else:
                self.update_last_failed_signed(email)
                self.password_entry.delete(0, 'end')
                messagebox.showerror("Error", "Incorrect password.")
        else:
            self.clear_login_fields()
            messagebox.showerror("Error", "Email not found.")

        cursor.close()
