import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from connector import cursor
from utils import fetch_and_display_image
import login,predict,train,validation

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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

        # Assuming fetch_and_display_image function is defined elsewhere in your code
        self.image_image_1 = fetch_and_display_image(self,"https://media1.tenor.com/m/bjLh2iYjW_cAAAAC/kau.gif", 1342, 107, 180, 209)
        self.image_image_2 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0, 214, 209)

        self.canvas.create_text(627.0, 85.0, anchor="nw", text="Homepage", fill="#000000", font=("Inter", 36 * -1))
        self.canvas.create_text(415.0, 190.0, anchor="nw", text="Welcome To Our Project Application", fill="#000000",
                                font=("Inter", 36 * -1))
        self.canvas.create_text(205.0, 285.0, anchor="nw",
                                text="Human Activity Recognition based on Generalized Efficient Layer Aggregation Network of YoloV9",
                                fill="#000000", font=("Inter", 24 * -1))
        self.canvas.create_text(204.0, 371.0, anchor="nw", text="\n", fill="#000000", font=("Inter", 20 * -1))
        self.canvas.create_text(211.0, 731.0, anchor="nw",
                                text="Abdulsalam Farun (Roll No. 2035687)"
                                     "\nKhalid Abdullah Alshehri (Roll No.2037000)"
                                     "\nMeshari Salim alshreif (Roll No. 2037018)"
                                     "\nAbdullah Abdulaziz Abushaigah (Roll No.2037460)",
                                fill="#000000", font=("Inter", 20 * -1))
        self.canvas.create_text(828.0, 730.0, anchor="nw",
                                text="Supervisor: Prof.Dr. Anton Satria Prabuwono"
                                     "\n\n\nco-Supervisor: Prof.Dr. Ahmad Hoirul Basori",
                                fill="#000000", font=("Inter", 20 * -1))
        self.canvas.create_text(534.0, 946.0, anchor="nw", text="(KING ABDULAZIZ UNIVERSITY)", fill="#011328",
                                font=("Inter", 24 * -1))
        self.canvas.create_text(211.0, 917.0, anchor="nw",
                                text="FACULTY OF COMPUTING AND INFORMATION TECHNOLOGY IN RABIGH ", fill="#011328",
                                font=("Inter", 24 * -1))

        button_1 = tk.Button(self, text="Train", font=35, borderwidth=0, highlightthickness=0,
                             command=lambda: controller.show_frame_with_auth(train.Train), relief="flat")
        button_1.place(x=314.0, y=486.0, width=300.0, height=85.0)

        button_2 = tk.Button(self, text="Predict", font=35, borderwidth=0, highlightthickness=0,
                             command=lambda: controller.show_frame_with_auth(predict.Predict), relief="flat")
        button_2.place(x=564.0, y=594.0, width=300.0, height=85.0)

        button_3 = tk.Button(self, text="Validate", font=35, borderwidth=0, highlightthickness=0,
                             command=lambda: controller.show_frame_with_auth(validation.Validation), relief="flat")
        button_3.place(x=826.0, y=486.0, width=300.0, height=85.0)

        self.canvas.create_text(624.0, 397.0, anchor="nw", text="Please Select", fill="#000000",
                                font=("Inter", 32 * -1))
        
        self.logout_btn = tk.Button(self, text="Login", font=30, bg="#FFFFFF", command=self.logout, borderwidth=0,
                                    highlightthickness=0, relief="flat")
        self.logout_btn.place(x=1276, y=921, width=131, height=50)
        self.update_logout_button_text()

    def logout(self):
        self.controller.set_session(None)
        self.update_logout_button_text()
        self.controller.show_frame(login.Login)

    def update_logout_button_text(self):
        session = self.controller.get_session()
        if session is None:
            self.logout_btn.config(text="Login")
        else:
            username = self.fetch_username_from_db(session)
            uname = f"User: {username}"
            self.logout_btn.config(text=uname)

    def fetch_username_from_db(self, user_id):
        try:
            query = "SELECT username FROM users WHERE session_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching username from database: {str(e)}")
            return None