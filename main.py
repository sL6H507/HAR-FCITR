import tkinter as tk
from tkinter import messagebox
import predict, train, validation,home,os

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

        for F in (home.HomePage, predict.Predict, train.Train,validation.Validation):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame_with_auth(home.HomePage)

    def set_session(self, session_id):
        self.session = session_id

    def get_session(self):
        return self.session

    def clear_session(self):
        self.session = None

    def show_frame_with_auth(self, page_name):
        frame = self.frames[page_name]
        self.geometry("1440x1024")
        self.center_window(1440, 1024)
        frame.tkraise()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

app = tkinterApp()
app.mainloop()
