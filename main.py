import tkinter as tk
from tkinter import messagebox,filedialog
from pathlib import Path
import os,sys,subprocess
import predict, train, home, login, register

OUTPUT_PATH = Path(__file__).parent
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

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

        for F in (home.HomePage, predict.Predict, train.Train, login.Login, register.Register):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(home.HomePage)

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




'''
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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

        self.image_image_1 = fetch_and_display_image(self,"https://media1.tenor.com/m/bjLh2iYjW_cAAAAC/kau.gif", 1342,107,180,209)
        self.image_image_2 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0,214,209)

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

        button_1 = Button(self, text="Train",font=35, borderwidth=0, highlightthickness=0,
                          command=lambda: controller.show_frame_with_auth(Train), relief="flat")
        button_1.place(x=316.0, y=499.0, width=300.0, height=85.0)

        button_2 = Button(self, text="Predict",font=35, borderwidth=0, highlightthickness=0,
                           command=lambda:controller.show_frame_with_auth(Predict),relief="flat")
        button_2.place(x=828.0, y=499.0, width=300.0, height=85.0)

        self.canvas.create_text(624.0, 397.0, anchor="nw", text="Please Select", fill="#000000",
                                font=("Inter", 32 * -1))
        
        self.logout_btn = tk.Button(self, text="Login", font=30, bg="#FFFFFF", command=self.logout, borderwidth=0,
                                    highlightthickness=0, relief="flat")
        self.logout_btn.place(x=1276, y=921, width=131, height=50)
        self.update_logout_button_text()

    def logout(self):
        self.controller.set_session(None)
        self.update_logout_button_text()
        self.controller.show_frame(Login)

    def update_logout_button_text(self):
        session = self.controller.get_session()
        if session is None:
            self.logout_btn.config(text="Login")
        else:
            username = self.fetch_username_from_db(session)
            uname = f"user: {username}"
            self.logout_btn.config(text=uname)

    def fetch_username_from_db(self, user_id):
        try:
            query = "SELECT username FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching username from database: {str(e)}")
            return None

class Train(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selected_device = tk.StringVar()
        self.selected_device.set(None)
        self.value_inside = tk.StringVar(self) 
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
        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0,214,209)

        self.canvas.create_text(316.0, 147.0, anchor="nw", text="Select Pre-Trained Model", fill="#000000",
                                font=("Inter", 32 * -1))

        predict_page_btn = tk.Button(self, text="For Predicting Click Here",font=30, borderwidth=0, highlightthickness=0,command= lambda : controller.show_frame_with_auth(Predict),
 relief="flat")
        predict_page_btn.place(x=594.0, y=905.0, width=259.0, height=82.0)

        self.Training_btn = tk.Button(self, text="Train",font=20, borderwidth=0, highlightthickness=0,
                                 command=self.start_training, relief="flat")
        self.Training_btn.place(x=659.0, y=448.0, width=148.0, height=39.0)

        self.entry_1 = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=316.0, y=384.0, width=502.0, height=43.0)
        self.canvas.create_text(316.0, 341.0, anchor="nw", text="Dataset (.yaml) location :", fill="#000000",
                                font=("Inter", 36 * -1))
        
        self.button_image_3 = fetch_image(self,"https://media.tenor.com/kEvgsQa811YAAAAM/dir.gif", 70, 36)
        datafile_btn = tk.Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0,
                                 command=self.select_data_file, relief="flat")
        datafile_btn.place(x=818.0, y=384.0, width=70.0, height=45.0)

        self.canvas.create_text(677.0, 47.0, anchor="nw", text="Train", fill="#000000", font=("Inter", 36 * -1))

        self.entry_2 = tk.Text(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=316.0, y=540.0, width=809.0, height=357.0)
        
        self.gpu_info = tk.Text(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.gpu_info.place(x=11.0, y=540.0, width=287.0, height=357.0)        
        self.update_gpu_info()


        self.canvas.create_text(316.0, 495.0, anchor="nw", text="Results", fill="#000000", font=("Inter", 32 * -1))
        self.canvas.create_text(11.0, 501.0, anchor="nw", text="GPU Info", fill="#000000", font=("Inter", 32 * -1))

        self.epochs_field = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.epochs_field.place(x=737.0, y=188.0, width=180.0, height=47.0)

        self.imgsz_field = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.imgsz_field.place(x=942.0, y=188.0, width=183.0, height=47.0)

        self.batchsz_field = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.batchsz_field.place(x=737.0, y=275.0, width=180.0, height=49.0)

        self.canvas.create_text(737.0, 147.0, anchor="nw", text="Epochs :", fill="#000000", font=("Inter", 32 * -1))
        self.canvas.create_text(942.0, 147.0, anchor="nw", text="Image Size :", fill="#000000", font=("Inter", 32 * -1))
        self.canvas.create_text(738.0, 237.0, anchor="nw", text="Batch Size :", fill="#000000", font=("Inter", 32 * -1))

        self.value_inside.set("Select a Pre-Trained Model") 
        options_list = ["YoloV9 Compact", "YoloV9 Extended", "Gelan Compact", "Gelan Extended","Other"] 

        model_menu = tk.OptionMenu(self, self.value_inside, *options_list,command=self.change_model) 
        model_menu.place(x=413.0, y=188.0, width=189.0, height=49.0)

        TensorBoard_btn = tk.Button(self, text="TensorBoard",font=20, borderwidth=0, highlightthickness=0,
                                   command=self.start_tensorboard, relief="flat")
        TensorBoard_btn.place(x=413.0, y=275.0, width=189.0, height=49.0)

        GPU = tk.Radiobutton(
            self,
            text="GPU",
            borderwidth=0,
            highlightthickness=0,
            variable=self.selected_device,
            value="GPU",
            relief="flat"
        )
        GPU.place(x=913.0, y=385.0, width=100.0, height=44.0)

        CPU = tk.Radiobutton(
            self,
            text="CPU",
            borderwidth=0,
            highlightthickness=0,
            variable=self.selected_device,
            value="CPU",
            relief="flat"
        )
        CPU.place(x=1025.0, y=385.0, width=100.0, height=44.0)

        self.canvas.create_text(913.0, 341.0, anchor="nw", text="Train Using :", fill="#000000",
                                font=("Inter", 36 * -1))
        self.homepage_btn = tk.Button(self, text="Home Page", font=40, bg="#FFFFFF", command=lambda: controller.show_frame_with_auth(HomePage), borderwidth=0,
                                    highlightthickness=0, relief="flat")
        self.homepage_btn.place(x=1276, y=921, width=131, height=50)

    def select_model_file(self):
        self.trainmodel_file_path = filedialog.askopenfilename(
            title="Select a Model File",
            filetypes=(("PyTorch Model Files", "*.pt"),)
        )
        if self.trainmodel_file_path:
            print(self.trainmodel_file_path)
        return self.trainmodel_file_path

    def select_data_file(self):
        self.data_file_path = filedialog.askopenfilename(
            title="Select a Yaml File",
            filetypes=(("Dataset information files", "*.yaml"),)
        )
        if self.data_file_path:
            self.entry_1.delete(0, tk.END)
            self.entry_1.insert(0, self.data_file_path)
        print(self.data_file_path)
        return self.data_file_path
    
    def select_logdir_file(self):
        self.logdir_file = filedialog.askdirectory(
            title="Select Log Directory"
        )        
        return self.logdir_file

    def change_model(self,selection):
        if selection == "Other":
            self.select_model_file()
        else:
            # Assign the appropriate pre-trained model path based on selection
            if selection == "YoloV9 Compact":
                self.trainmodel_file_path = "yolov9c.pt"
            elif selection == "YoloV9 Extended":
                self.trainmodel_file_path = "yolov9e.pt"
            elif selection == "Gelan Compact":
                self.trainmodel_file_path = "gelan-c.pt"
            elif selection == "Gelan Extended":
                self.trainmodel_file_path = "gelan-e.pt"
            else:
                self.trainmodel_file_path = None
                tk.messagebox.showwarning(title="Training", message="Wrong Selection")


    def start_training(self):
        try:
            epochs = int(self.epochs_field.get())
            batch_size = int(self.batchsz_field.get())
            img_size = int(self.imgsz_field.get())
            device = "cpu" if self.selected_device.get() == "CPU" else "0"
            if self.trainmodel_file_path and self.data_file_path and epochs and img_size and batch_size:
                self.Training_btn.configure(state="disabled")
                command = [sys.executable, "-c", f"""
import subprocess
from ultralytics import YOLO

def main():
    model_path = '{self.trainmodel_file_path}'
    data_path = '{self.data_file_path}'
    epochs = {epochs}
    img_size = {img_size}
    batch_size = {batch_size}
    device = '{device}'
    
    model = YOLO(model_path)
    model.train(device=device, data=data_path, epochs=epochs, imgsz=img_size, batch=batch_size)

if __name__ == '__main__':
    main()
"""]
                
                # Run the training script in a separate thread to keep the GUI responsive
                thread = threading.Thread(target=self.run_training, args=(command,))
                thread.start()
            else:
                tk.messagebox.showwarning(title="Training", message="Please fill in all required fields.")
        except ValueError:
            tk.messagebox.showwarning(title="Training", message="Integer only.")
        except NameError:
            tk.messagebox.showwarning(title="Training", message="Please fill in all required fields.")
        except AttributeError:
            tk.messagebox.showwarning(title="Training", message="Please fill in all required fields.")

    def run_training(self, command):
        # Clear previous output
        self.entry_2.delete("1.0", tk.END)
        
        # Open subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        
        # Read output line by line and update the GUI
        for line in iter(process.stdout.readline, ""):
            self.entry_2.insert(tk.END, line)
            self.entry_2.see(tk.END)
            self.update_idletasks()  # Update the GUI to show new content
        
        # Close the process and update the GUI once more
        process.stdout.close()
        process.wait()
        self.entry_2.insert(tk.END, "\nTraining finished.\n")
        self.entry_2.see(tk.END)
        self.Training_btn.configure(state="active")


    def update_gpu_info(self):
        # Clear previous GPU information
        self.gpu_info.delete("1.0", tk.END)

        # Get GPU information
        gpu_info = self.get_gpu_info()

        # Update text widget with new GPU information
        self.gpu_info.insert(tk.END, gpu_info)

        # Schedule the next update after 5 seconds (5000 milliseconds)
        self.after(5000, self.update_gpu_info)

    def get_gpu_info(self):
        gpus = nvsmi.get_gpus()
        gpu_info = ""
        for gpu in gpus:
            gpu_info += f"GPU: {gpu.id}\n"
            gpu_info += f"Name: {gpu.name}\n"
            gpu_info += f"Memory Total: {gpu.mem_total} MiB\n"
            gpu_info += f"Memory Used: {gpu.mem_used} MiB\n"
            gpu_info += f"Memory Free: {gpu.mem_free} MiB\n"
            gpu_info += f"Utilization: {gpu.gpu_util}%\n"
            gpu_info += f"Temperature: {gpu.temperature} C\n"
        return gpu_info
    
    def start_tensorboard(self):
        self.select_logdir_file()
        if not self.logdir_file:
            tk.messagebox.showerror("TensorBoard Error", "Please select a log directory.")
            return    
        try:            
            print(self.logdir_file)
            tensorboard_command = ["tensorboard", "--logdir", self.logdir_file]
            subprocess.Popen(tensorboard_command)
            tk.messagebox.showinfo("TensorBoard", f"TensorBoard started successfully!\nhttp://localhost:6006 to use\nLog directory: {self.logdir_file}")
        except FileNotFoundError:
            tk.messagebox.showerror("TensorBoard Error", "TensorBoard executable not found. Make sure TensorBoard is installed and in your PATH.")
        except Exception as e:
            tk.messagebox.showerror("TensorBoard Error", f"Error starting TensorBoard: {str(e)}")

class Predict(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selected_device = tk.StringVar()
        self.selected_device.set(None)

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
        self.canvas.create_text(305.0,649.0,anchor="nw",text="Live Footage",fill="#000000",            font=("Inter", 36 * -1)        )
        self.canvas.create_text(660.0,649.0,anchor="nw",text="Video",fill="#000000",            font=("Inter", 36 * -1)        )
        self.canvas.create_text(974.0,649.0,anchor="nw",text="Image",fill="#000000",            font=("Inter", 36 * -1)        )

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
        predict_btn = tk.Button(self, text="Predict",font=20, borderwidth=0, highlightthickness=0,
                                   command=self.p_predict, relief="flat")
        predict_btn.place(
            x=957.0,
            y=294.0,
            width=179.0,
            height=36.0
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

        self.modeldir_btn_img = fetch_image(self,"https://media.tenor.com/kEvgsQa811YAAAAM/dir.gif", 70, 36)
        modeldir = tk.Button(self, image=self.modeldir_btn_img, borderwidth=0, highlightthickness=0,
                                   command=self.select_model_file, relief="flat")
        modeldir.place(x=771.0,y=294.0,width=70.0,height=36.0)

        nextpage_btn = tk.Button(self, text="For Training Click Here",font=30, borderwidth=0, highlightthickness=0,
                                   command=lambda: controller.show_frame_with_auth(Train), relief="flat")
        nextpage_btn.place(
            x=602.0,
            y=910.0,
            width=237.0,
            height=82.0
        )
        self.entry_3 = tk.Text(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.entry_3.place(
            x=304.0,
            y=427.0,
            width=832.0,
            height=151.0
        )

        self.canvas.create_text(
            304.0,
            398.0,
            anchor="nw",
            text="Results",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.homepage_btn = tk.Button(self, text="Home Page", font=40, bg="#FFFFFF", command=lambda: controller.show_frame_with_auth(HomePage), borderwidth=0,
                                    highlightthickness=0, relief="flat")
        self.homepage_btn.place(x=1276, y=910, width=131, height=50)

    def select_model_file(self):
        self.model_file_path = filedialog.askopenfilename(
            title="Select a Model File",
            filetypes=(("PyTorch Model Files", "*.pt"),)
        )
        if self.model_file_path:
            self.entry_1.delete(0, tk.END)
            self.entry_1.insert(0, self.model_file_path)
        return self.model_file_path
    def select_video_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=(("Video Files (.mp4;.avi)", "*.mp4;*.avi"),)
        )
        print(self.file_path)
        return self.file_path


    def select_image_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=(("Image Files (.png;.jpg;.jpeg)", "*.png;*.jpg;*.jpeg"),)
        )
        print(self.file_path)
        return self.file_path

    def p_predict(self):
        confidence = float(self.confscale.get()) / 100        
        iou = float(self.iouscale.get()) / 100
        try:
            if self.model_file_path and self.file_path:
            #model = YOLO(model_file_path).predict(file_path,show=True,save=True, conf=confidence)
                self.entry_3.delete(1.0, tk.END)  # Clear previous results
                self.entry_3.insert(tk.END, YOLO(self.model_file_path).predict(self.file_path, show=True, save=True, conf=confidence,iou=iou))
            else:
                tk.messagebox.showwarning(title="Predict", message="Model file or input file not selected.")
        except Exception as er:
            tk.messagebox.showerror(title="Predict", message=er)

    def cam_predict(self):
        cap = cv2.VideoCapture(0)
        confidence = float(self.confscale.get()) / 100          
        iou = float(self.iouscale.get()) / 100
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 60)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            try:
                if self.model_file_path:
                    results = YOLO(self.model_file_path).predict(source=0, show=True, save=True, conf=confidence,iou=iou)
                    self.entry_3.delete(1.0, tk.END)  # Clear previous results
                    self.entry_3.insert(tk.END, results)
                    cv2.imshow("frame", results[0].plot())
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    tk.messagebox.showwarning(title="Predict", message="Model file or input file not selected.")
                    break
            except Exception as er:
                tk.messagebox.showerror(title="Predict", message=str(er))
                break

        cap.release()
        cv2.destroyAllWindows()

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mydb = mydb

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
        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0,214,209)
        self.image_image_2 = fetch_and_display_image(self,"https://media.tenor.com/bjLh2iYjW_cAAAAM/kau.gif", 1180.0, 107,180,209)

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
                                   command=lambda : controller.show_frame(Register), relief="flat")
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

    def validate_and_login(self):

        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            messagebox.showerror("Error", "All fields must be filled.")
            return
        hashed_password = self.hash_password(password)
        cursor = self.mydb.cursor()
        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result:
            stored_password = result[3]
            if hashed_password == stored_password:
                self.update_last_signed(email)
                messagebox.showinfo("Success", "Login successful!")
                self.clear_login_fields()           
                user_id = result[0]
                self.controller.set_session(user_id)
                self.controller.show_frame_with_auth(HomePage)
            else:                
                self.update_last_failed_signed(email)                
                self.password_entry.delete(0, 'end')
                messagebox.showerror("Error", "Incorrect password.")
        else:    
            self.clear_login_fields()   
            messagebox.showerror("Error", "Email not found.")

        cursor.close()

class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mydb = mydb
        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 1280,
            width = 1440,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0,214,209)
        self.image_image_2 = fetch_and_display_image(self,"https://media.tenor.com/bjLh2iYjW_cAAAAM/kau.gif", 1180.0, 107,180,209)

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
                            command=lambda: controller.show_frame(Login), relief="flat")
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

    def hash_password(self,password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def clear_registration_fields(self):
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def validate_and_register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not name or not email or not password:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        if "@" not in email:
            messagebox.showerror("Error", "Invalid email address.")
            return

        if len(password) < 8 or len(password) > 24:
            messagebox.showerror("Error", "Password must be between 8-24 characters.")
            return

        hashed_password = self.hash_password(password)
        
        cursor = mydb.cursor()
        sql = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)"
        val = (email, name, hashed_password)
        
        try:
            cursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.clear_registration_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
'''

app = tkinterApp()
app.mainloop()
