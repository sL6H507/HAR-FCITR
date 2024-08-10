import time
import tkinter as tk
from tkinter import Canvas, Button, filedialog, Scale, Text, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from io import BytesIO
from utils import fetch_and_display_image, fetch_image
import requests
import cv2
import home
import train
import wget
import os
from ultralytics import YOLO


class Predict(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.model_file_path = None
        self.value_model_inside = tk.StringVar(self)
        self.file_path = None

        self.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_text(
            659.0,
            72.0,
            anchor="nw",
            text="Predict",
            fill="#000000",
            font=("Inter", 36 * -1)
        )
        self.canvas.create_text(
            568.0,
            581.0,
            anchor="nw",
            text="Select An option ",
            fill="#000000",
            font=("Inter", 36 * -1)
        )
        self.canvas.create_text(
            304.0, 641.0, anchor="nw", text="Live Footage", fill="#000000", font=("Inter", 36 * -1))
        self.canvas.create_text(
            659.0, 641.0, anchor="nw", text="Video", fill="#000000", font=("Inter", 36 * -1))
        self.canvas.create_text(
            973.0, 641.0, anchor="nw", text="Image", fill="#000000", font=("Inter", 36 * -1))

        self.value_model_inside.set("Select a Model")
        options_model_list = ["Human Action Recogition", "Other"]
        model_menu = tk.OptionMenu(
            self, self.value_model_inside, *options_model_list, command=self.change_model)
        model_menu.place(x=385.0, y=242.0, width=189.0, height=49.0)

        self.canvas.create_text(
            304.0,
            194.0,
            anchor="nw",
            text="Model (.pt) Selection :",
            fill="#000000",
            font=("Inter", 36 * -1)
        )

        self.confscale = Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=200,
            bd=0,
            bg="#F8F8F8",
            fg="#000716",
            highlightthickness=0,
            resolution=1
        )
        self.confscale.place(
            x=304.0,
            y=326.0
        )
        self.confscale.set(50)

        self.iouscale = Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=200,
            bd=0,
            bg="#F8F8F8",
            fg="#000716",
            highlightthickness=0,
            resolution=1
        )
        self.iouscale.place(
            x=525.0,
            y=326.0
        )
        self.iouscale.set(50)

        self.canvas.create_text(
            304.0,
            299.0,
            anchor="nw",
            text="Confidence :",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.canvas.create_text(
            304.0,
            378.0,
            anchor="nw",
            text="Results :",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.canvas.create_text(
            525.0,
            299.0,
            anchor="nw",
            text="Overlapping:",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.result_entry = Text(
            self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.result_entry.place(
            x=303.0,
            y=407.0,
            width=832.0,
            height=151.0
        )

        predict_btn = tk.Button(self, text="Predict", font=("Inter", 20), borderwidth=0, highlightthickness=0,
                                command=self.imgvid_predict, relief="flat")
        predict_btn.place(
            x=956.0,
            y=242.0,
            width=179.0,
            height=36.0
        )

        nextpage_btn = tk.Button(self, text="Training", font=("Inter", 15), borderwidth=0, bg="#FFFFFF",
                                 highlightthickness=0, command=lambda: controller.show_frame_with_auth(train.Train), relief="flat")
        nextpage_btn.place(
            x=18.0,
            y=902.0,
            width=131.0,
            height=50.0
        )

        linkprediction = tk.Button(self, text="Prediction using Link", font=("Inter", 15), borderwidth=0,
                                   highlightthickness=0, command=self.show_link_prediction_dialog,
                                   relief="flat")
        linkprediction.place(
            x=729.0,
            y=902.0,
            width=237.0,
            height=82.0
        )

        directoryprediction = tk.Button(self, text="Prediction Directory", font=("Inter", 15), borderwidth=0,
                                        highlightthickness=0, command=self.directoryprediction,
                                        relief="flat")
        directoryprediction.place(
            x=436.0,
            y=902.0,
            width=237.0,
            height=82.0
        )

        self.homepage_btn = tk.Button(self, text="Home Page", font=("Inter", 15), bg="#FFFFFF",
                                      command=lambda: controller.show_frame_with_auth(home.HomePage), borderwidth=0,
                                      highlightthickness=0, relief="flat")
        self.homepage_btn.place(x=1289, y=931, width=131, height=50)

        self.image_image_1 = fetch_and_display_image(
            self, "https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0, 214, 209)

        self.photoimage = fetch_image(
            self, "https://media.tenor.com/Zv5dIqsnvtcAAAAM/photo.gif", 221, 209),
        predictimage = tk.Button(self, image=self.photoimage, borderwidth=0,
                                 highlightthickness=0, command=self.select_image_file, relief="flat")
        predictimage.place(x=914.0, y=685.0, width=221.0, height=209.0)

        self.liveimage = fetch_image(
            self, "https://media.tenor.com/LfYVxf_SjysAAAAM/cam.gif", 221, 209)
        self.predictlive = tk.Button(self, borderwidth=0, highlightthickness=0,
                                     image=self.liveimage, command=self.cam_predict, relief="flat")
        self.predictlive.place(x=303.0, y=685.0, width=221.0, height=209.0)

        self.predictvid_img = fetch_image(
            self, "https://media.tenor.com/Co-LVRF8ZwEAAAAM/cam.gif", 221, 209)
        predictvid = tk.Button(self, image=self.predictvid_img, borderwidth=0,
                               highlightthickness=0, command=self.select_video_file, relief="flat")
        predictvid.place(x=597.0, y=685.0, width=221.0, height=209.0)

    def select_model_file(self):
        self.model_file_path = filedialog.askopenfilename(
            title="Select a Model File",
            filetypes=(("PyTorch Model Files", "*.pt"),)
        )
        if self.model_file_path:
            print(self.model_file_path)

    def change_model(self, selection):
        if selection == "Other":
            self.select_model_file()
        else:
            if selection == "Human Action Recogition":
                self.result_entry.delete(1.0, tk.END)

                # Filename and URL
                filename = 'HAR.pt'
                url = 'https://drive.usercontent.google.com/download?id=10u18T9FVRo6mY9xcErX5MMMDM0wqBvl0&export=download&authuser=0&confirm=t&uuid=85fd1a27-fbb0-4ec8-92de-b7358f676dd9&at=APZUnTWbQCNNF8Rf5sHm-vbTn14M%3A1723305433606'

                # Check if file exists
                if os.path.exists(filename):
                    self.result_entry.insert(
                        tk.END, f"File already exists: {filename}")
                    self.model_file_path = filename
                else:
                    # Download the file if it does not exist
                    downloaded_file = wget.download(url, filename)
                    self.result_entry.insert(tk.END, downloaded_file)
                    self.model_file_path = downloaded_file
            else:
                self.model_file_path = None
                tk.messagebox.showwarning(
                    title="Training", message="Wrong Selection")

    def select_video_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=(("Video Files (.mp4;.avi)",
                       "*.mp4;*.avi;*.mpeg;*.webm;*.mpg;*.mov;*.gif;*.asf;*.mkv;*.m4v"),)
        )

    def select_image_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=(("Image Files (.png;.jpg;.jpeg)",
                       "*.png;*.jpg;*.jpeg;*.dng;*.tiff;*.tif;*.webp;*.bmp;*.mpo"),)
        )

    def imgvid_predict(self):
        confidence = float(self.confscale.get()) / 100
        iou = float(self.iouscale.get()) / 100

        try:
            if self.model_file_path and self.file_path:
                self.result_entry.delete(1.0, tk.END)  # Clear previous results
                results = YOLO(self.model_file_path).predict(self.file_path, show=True, save=True, conf=confidence, iou=iou, imgsz=480)

                results_text = f"File name : {self.file_path}\n\nSpeed : {results[0].speed}\n\nSaved Path : {results[0].save_dir}\n"

                # Show prediction probabilities
                for i, (cls, conf) in enumerate(zip(results[0].boxes.cls, results[0].boxes.conf)):
                    results_text += f"\nPrediction {i+1}:\n"
                    results_text += f"Class: {cls}, Confidence: {conf*100:.2f}%\n"

                self.result_entry.insert(tk.END, results_text)
            else:
                messagebox.showwarning(
                    title="Predict", message="Model file or input file not selected.")
        except Exception as er:
            messagebox.showerror(title="Predict", message=str(er))

    def cam_predict(self):
        if not self.model_file_path:
            messagebox.showwarning(
                title="Predict", message="Model file not selected.")
            return
        model = YOLO(model=self.model_file_path)
        confidence = float(self.confscale.get()) / 100
        iou = float(self.iouscale.get()) / 100

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        cap.set(cv2.CAP_PROP_FPS, 15)

        # Generate a dynamic file name using the current timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f'HAR_{timestamp}.mp4'

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(file_name, fourcc, 30.0, (800, 600))

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            self.result_entry.delete(1.0, tk.END)
            results = model.predict(frame, iou=iou, conf=confidence)

            results_text = ""
            # Show prediction probabilities with class names
            for i, (cls, conf) in enumerate(zip(results[0].boxes.cls, results[0].boxes.conf)):
                class_name = model.names[int(cls)]
                results_text += f"\nPrediction {i+1}:\n"
                results_text += f"Class: {class_name}, Confidence: {conf*100:.2f}%\n"

            self.result_entry.insert(tk.END, results_text)

            # Write the frame to the video file
            out.write(results[0].plot())

            cv2.imshow("frame", results[0].plot())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()  # Release the video writer
        cv2.destroyAllWindows()


    def show_link_prediction_dialog(self):
        confidence = float(self.confscale.get()) / 100
        iou = float(self.iouscale.get()) / 100
        link = simpledialog.askstring("Link Prediction", "Enter the link for prediction:")
        
        if self.model_file_path:
            if not link:
                messagebox.showwarning(title="Predict", message="No link provided.")
                return
            
            try:
                self.result_entry.delete(1.0, tk.END)
                img = wget.download(link)
                model = YOLO(self.model_file_path)
                results = model.predict(img, show=True, save=True, conf=confidence, iou=iou, imgsz=480)
                
                results_text = f"File name : {self.file_path}\n\nSpeed : {results[0].speed}\n\nSaved Path : {results[0].save_dir}\n"

                # Show prediction probabilities with class names
                for i, (cls, conf) in enumerate(zip(results[0].boxes.cls, results[0].boxes.conf)):
                    class_name = model.names[int(cls)]
                    results_text += f"\nPrediction {i+1}:\n"
                    results_text += f"Class: {class_name}, Confidence: {conf*100:.2f}%\n"

                self.result_entry.insert(tk.END, results_text)

            except Exception as er:
                # Handle specific exceptions related to video stream
                if 'Video stream unresponsive' in str(er):
                    messagebox.showerror(title="Predict", message="Video stream unresponsive, please check your IP camera connection.")
                else:
                    messagebox.showerror(title="Predict", message=str(er))
        else:
            messagebox.showwarning(title="Predict", message="Model file not selected.")


    def directoryprediction(self):
        confidence = float(self.confscale.get()) / 100
        iou = float(self.iouscale.get()) / 100
        directory = filedialog.askdirectory(
            title="Select Directory for Prediction")

        if self.model_file_path:
            try:
                if directory:
                    self.result_entry.delete(1.0, tk.END)
                    model = YOLO(self.model_file_path)
                    results_text = ""

                    for filename in os.listdir(directory):
                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            results = model.predict(
                                source=file_path, save=True, conf=confidence, iou=iou, imgsz=480, save_conf=True, save_txt=True)

                            results_text += f"File name : {filename}\n\nSpeed : {results[0].speed}\n\nSaved Path : {results[0].save_dir}\n"

                            # Show prediction probabilities with class names
                            for i, (cls, conf) in enumerate(zip(results[0].boxes.cls, results[0].boxes.conf)):
                                class_name = model.names[int(cls)]
                                results_text += f"\nPrediction {i+1}:\n"
                                results_text += f"Class: {class_name}, Confidence: {conf*100:.2f}%\n"

                    self.result_entry.insert(tk.END, results_text)
                else:
                    messagebox.showwarning(
                        title="Predict", message="No directory selected.")
            except Exception as er:
                messagebox.showerror(title="Predict", message=str(er))
        else:
            messagebox.showwarning(
                title="Predict", message="Model file not selected.")

