import tkinter as tk
from tkinter import messagebox,filedialog
from pathlib import Path
import os,sys,subprocess
import predict, train, home, login, register,validation

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.session = None  
        self.title("Project - 2")
        self.geometry("1440x1024")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (home.HomePage, predict.Predict, train.Train, login.Login, register.Register,validation.Validation):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(validation.Validation)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name in [login.Login, register.Register]:
            self.geometry("1280x720")
            self.center_window(1280, 720)
        else:
            self.geometry("1440x1024")
            self.center_window(1440, 1024)
        frame.tkraise()

    def set_session(self, session_id):
        self.session = session_id

    def get_session(self):
        return self.session

    def clear_session(self):
        self.session = None

    def show_frame_with_auth(self, page_name):
        if self.get_session() is None:
            messagebox.showerror("Error", "You're not signed in")
            self.show_frame(login.Login)
        else:
            self.show_frame(page_name)
            if page_name == home.HomePage:
                self.frames[home.HomePage].update_logout_button_text()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

app = tkinterApp()
app.mainloop()
