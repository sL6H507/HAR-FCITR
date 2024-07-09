import tkinter as tk
from tkinter import Canvas, Button, filedialog, Scale, Text, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from io import BytesIO
from utils import fetch_and_display_image,fetch_image
import requests,cv2,home,train
from ultralytics import YOLO 

class Predict(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.model_file_path = None
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
            633.0,
            72.0,
            anchor="nw",
            text="Predict",
            fill="#000000",
            font=("Inter", 36 * -1)
        )
        self.canvas.create_text(
            569.0,
            589.0,
            anchor="nw",
            text="Select An option ",
            fill="#000000",
            font=("Inter", 36 * -1)
        )
        self.canvas.create_text(305.0, 649.0, anchor="nw", text="Live Footage", fill="#000000", font=("Inter", 36 * -1))
        self.canvas.create_text(660.0, 649.0, anchor="nw", text="Video", fill="#000000", font=("Inter", 36 * -1))
        self.canvas.create_text(974.0, 649.0, anchor="nw", text="Image", fill="#000000", font=("Inter", 36 * -1))

        self.entry_1 = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.entry_1.place(
            x=304.0,
            y=294.0,
            width=467.0,
            height=34.0
        )

        self.canvas.create_text(
            304.0,
            254.0,
            anchor="nw",
            text="Model (.pt) location :",
            fill="#000000",
            font=("Inter", 36 * -1)
        )

        self.modeldir_btn_img = fetch_image(self,"https://media.tenor.com/kEvgsQa811YAAAAM/dir.gif", 70, 36)
        modeldir = tk.Button(self, image=self.modeldir_btn_img, borderwidth=0, highlightthickness=0,
                                   command=self.select_model_file, relief="flat")
        modeldir.place(x=771.0, y=294.0, width=70.0, height=36.0)

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
            y=357.0
        )

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
            y=357.0
        )

        self.canvas.create_text(
            304.0,
            330.0,
            anchor="nw",
            text="Confidence :",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.canvas.create_text(
            525.0,
            330.0,
            anchor="nw",
            text="Intersection Over Union (IoU):",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.result_entry = Text(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.result_entry.place(
            x=304.0,
            y=427.0,
            width=832.0,
            height=151.0
        )

        predict_btn = tk.Button(self, text="Predict", font=("Inter", 20), borderwidth=0, highlightthickness=0,
                                command=self.p_predict, relief="flat")
        predict_btn.place(
            x=957.0,
            y=294.0,
            width=179.0,
            height=36.0
        )

        nextpage_btn = tk.Button(self, text="For Training Click Here", font=("Inter", 15), borderwidth=0,
                                 highlightthickness=0, command=lambda: controller.show_frame_with_auth(train.Train),
                                 relief="flat")
        nextpage_btn.place(
            x=602.0,
            y=910.0,
            width=237.0,
            height=82.0
        )

        linkprediction = tk.Button(self, text="Predicting Link", font=("Inter", 15), borderwidth=0,
                                 highlightthickness=0, command=lambda: controller.show_frame_with_auth(train.Train),
                                 relief="flat")
        linkprediction.place(
            x=296.0,
            y=910.0,
            width=237.0,
            height=82.0
        )

        self.homepage_btn = tk.Button(self, text="Home Page", font=("Inter", 15), bg="#FFFFFF",
                                      command=lambda: controller.show_frame_with_auth(home.HomePage), borderwidth=0,
                                      highlightthickness=0, relief="flat")
        self.homepage_btn.place(x=1276, y=910, width=131, height=50)


        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0,214,209)

        self.photoimage=fetch_image(self,"https://media.tenor.com/Zv5dIqsnvtcAAAAM/photo.gif",221,209),
        predictimage = tk.Button(self, image=self.photoimage, borderwidth=0, highlightthickness=0,command=self.select_image_file, relief="flat")
        predictimage.place(x=915.0,y=693.0,width=221.0,height=209.0)

        self.liveimage = fetch_image(self,"https://media.tenor.com/LfYVxf_SjysAAAAM/cam.gif", 221, 209)
        self.predictlive = tk.Button(self, borderwidth=0, highlightthickness=0, image=self.liveimage, command=self.cam_predict, relief="flat")
        self.predictlive.place(x=304.0, y=693.0, width=221.0, height=209.0)

        self.predictvid_img = fetch_image(self,"https://media.tenor.com/Co-LVRF8ZwEAAAAM/cam.gif", 221, 209)
        predictvid = tk.Button(self, image=self.predictvid_img, borderwidth=0, highlightthickness=0,command=self.select_video_file, relief="flat")
        predictvid.place(x=599.0,y=693.0,width=221.0,height=209.0)

    def select_model_file(self):
        self.model_file_path = filedialog.askopenfilename(
            title="Select a Model File",
            filetypes=(("PyTorch Model Files", "*.pt"),)
        )
        if self.model_file_path:
            self.entry_1.delete(0, tk.END)
            self.entry_1.insert(0, self.model_file_path)

    def select_video_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=(("Video Files (.mp4;.avi)", "*.mp4;*.avi;*.mpeg;*.webm;*.mpg;*.mov;*.gif;*.asf;*.mkv;*.m4v"),)
        )

    def select_image_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=(("Image Files (.png;.jpg;.jpeg)", "*.png;*.jpg;*.jpeg;*.dng;*.tiff;*.tif;*.webp;*.bmp;*.mpo"),)
        )

    def p_predict(self):
        confidence = float(self.confscale.get()) / 100
        iou = float(self.iouscale.get()) / 100

        try:
            if self.model_file_path and self.file_path:
                self.result_entry.delete(1.0, tk.END)  # Clear previous results
                results = YOLO(self.model_file_path).predict(self.file_path, show=True, save=True, conf=confidence,
                                                             iou=iou,imgsz=640)
                self.result_entry.insert(tk.END, results)
            else:
                messagebox.showwarning(title="Predict", message="Model file or input file not selected.")
        except Exception as er:
            messagebox.showerror(title="Predict", message=str(er))


    def cam_predict(self):
        # Retrieve confidence and IOU values from the scales
        confidence = float(self.confscale.get()) / 100
        iou = float(self.iouscale.get()) / 100

        # Load the YOLO model
        if not self.model_file_path:
            messagebox.showwarning(title="Predict", message="Model file not selected.")
            return

        model = YOLO(self.model_file_path)

        # Open the webcam
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  # Lower resolution
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)  # Lower resolution
        cap.set(cv2.CAP_PROP_FPS, 60)  # Lower FPS

        if not cap.isOpened():
            print("Failed to open webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Perform prediction using YOLO
            results = model.predict(source=frame, conf=confidence, iou=iou, imgsz=800)

            # Display the frame with predictions
            if results and results[0]:
                cv2.imshow("frame", results[0].plot())
            else:
                cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

    def show_link_prediction_dialog(self):
        confidence = float(self.confscale.get()) / 100
        iou = float(self.iouscale.get()) / 100
        link = simpledialog.askstring("Link Prediction", "Enter the link for prediction:")
        if self.model_file_path:
            try:
                if link:
                    self.result_entry.delete(1.0, tk.END)  # Clear previous results
                    results = YOLO(self.model_file_path).predict(link, show=True, save=True, conf=confidence,
                                                                iou=iou,imgsz=640)
                    self.result_entry.insert(tk.END, results)
                else:
                    messagebox.showwarning(title="Predict", message="Model file or input file not selected.")
            except Exception as er:
                messagebox.showerror(title="Predict", message=str(er))
