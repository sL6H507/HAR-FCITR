import tkinter as tk
from tkinter import Canvas, Button, filedialog, Scale, Text, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from io import BytesIO
from utils import fetch_and_display_image,fetch_image
import requests,home,train,subprocess,threading,sys,torch,nvsmi
from ultralytics import YOLO 

class Validation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.model_file_path = None
        self.datasetfile_path = None
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

        self.canvas.create_text(
            659.0,
            72.0,
            anchor="nw",
            text="Validate",
            fill="#000000",
            font=("Inter", 36 * -1)
        )

        self.modelentry = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.modelentry.place(x=304.0,y=234.0,width=453.0,height=36.0)
        self.dataset_entry = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.dataset_entry.place(x=305.0,y=310.0,width=452.0,height=36.0)
        self.imgsz_entry = tk.Entry(self, bd=0, bg="#E3E3E3", fg="#000716", highlightthickness=0)
        self.imgsz_entry.place(x=989.0,y=388.0,width=148.0,height=36.0)
        self.batchsz_entry = tk.Entry(self, bd=0, bg="#E3E3E3", fg="#000716", highlightthickness=0)
        self.batchsz_entry.place(x=765.0,y=388.0,width=148.0,height=36.0)

        self.canvas.create_text(
            305.0,
            194.0,
            anchor="nw",
            text="Model (.pt) location :",
            fill="#000000",
            font=("Inter", 36 * -1)
        )

        self.canvas.create_text(
            305.0,
            270.0,
            anchor="nw",
            text="Dataset (.yaml) location :",
            fill="#000000",
            font=("Inter", 36 * -1)
        )

        self.canvas.create_text(
            304.0,
            444.0,
            anchor="nw",
            text="Results",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.modeldir_btn_img = fetch_image(self,"https://media.tenor.com/kEvgsQa811YAAAAM/dir.gif", 70, 36)
        modeldir = tk.Button(self, image=self.modeldir_btn_img, borderwidth=0, highlightthickness=0,
                                   command=self.select_model_file, relief="flat")
        modeldir.place(x=757.0, y=234.0, width=70.0, height=36.0)

        self.datasetdir_btn_img = fetch_image(self,"https://media.tenor.com/kEvgsQa811YAAAAM/dir.gif", 70, 36)
        datasetdir_btn = tk.Button(self, image=self.datasetdir_btn_img, borderwidth=0, highlightthickness=0,
                                   command=self.select_dataset_file, relief="flat")
        datasetdir_btn.place(x=757.0, y=310.0, width=70.0, height=36.0)

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
            x=305.0,
            y=388.0
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
            y=388.0
        )

        self.canvas.create_text(
            304.0,
            358.0,
            anchor="nw",
            text="Confidence :",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.canvas.create_text(
            526.0,
            358.0,
            anchor="nw",
            text="Overlapping:",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.canvas.create_text(
            765.0,
            358.0,
            anchor="nw",
            text="Image Size:",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.canvas.create_text(
            989.0,
            358.0,
            anchor="nw",
            text="Batch Size:",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.result_entry = Text(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        self.result_entry.place(
            x=304.0,
            y=473.0,
            width=832.0,
            height=360.0
        )

        nextpage_btn = tk.Button(self, text="Training", font=("Inter", 15), borderwidth=0, bg="#FFFFFF",
                                 highlightthickness=0, command=lambda: controller.show_frame_with_auth(train.Train), relief="flat")
        nextpage_btn.place(
            x=19.0,
            y=860.0,
            width=131.0,
            height=50.0
        )

        self.validate = tk.Button(self, text="Validate", font=("Inter", 15), borderwidth=0,
                                 highlightthickness=0, command=self.start_validating,
                                 relief="flat")
        self.validate.place(
            x=598.0,
            y=860.0,
            width=237.0,
            height=82.0
        )

        self.homepage_btn = tk.Button(self, text="Home Page", font=("Inter", 15), bg="#FFFFFF",
                                      command=lambda: controller.show_frame_with_auth(home.HomePage), borderwidth=0,
                                      highlightthickness=0, relief="flat")
        self.homepage_btn.place(x=1290, y=860, width=131, height=50)


        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0,214,209)
        self.GPU = tk.Radiobutton(
            self,
            text="GPU",
            borderwidth=0,
            highlightthickness=0,
            variable=self.selected_device,
            value="GPU",
            relief="flat",
            )
        self.GPU.place(x=918.0, y=284.0, width=100.0, height=44.0)

        self.CPU = tk.Radiobutton(
            self,
            text="CPU",
            borderwidth=0,
            highlightthickness=0,
            variable=self.selected_device,
            value="CPU",
            relief="flat"
        )
        self.CPU.place(x=1029.0, y=284.0, width=100.0, height=44.0)
        
        self.canvas.create_text(929.0, 245.0, anchor="nw", text="Train Using :", fill="#000000",
                                font=("Inter", 36 * -1))
        
        self.canvas.create_text(11.0, 444.0, anchor="nw", text="GPU Info", fill="#000000", font=("Inter", 32 * -1))
        self.gpu_info = tk.Text(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.gpu_info.place(x=11.0, y=480.0, width=287.0, height=357.0)
        self.update_gpu_info()
        self.checkgpu()
        nextpage_btn = tk.Button(self, text="Training", font=("Inter", 15), borderwidth=0, bg="#FFFFFF",
                                 highlightthickness=0, command=lambda: controller.show_frame_with_auth(train.Train), relief="flat")
        nextpage_btn.place(
            x=19.0,
            y=860.0,
            width=131.0,
            height=50.0
        )
    def select_model_file(self):
        self.model_file_path = filedialog.askopenfilename(
            title="Select a Model File",
            filetypes=(("PyTorch Model Files", "*.pt"),)
        )
        if self.model_file_path:
            self.modelentry.delete(0, tk.END)
            self.modelentry.insert(0, self.model_file_path)

    def select_dataset_file(self):
        self.datasetfile_path = filedialog.askopenfilename(
            title="Select a Yaml File",
            filetypes=(("Dataset information files", "*.yaml"),)
        )
        if self.datasetfile_path:
            self.dataset_entry.delete(0, tk.END)
            self.dataset_entry.insert(0, self.model_file_path)
    
    def start_validating(self):
        try:
            confidence = float(self.confscale.get()) / 100
            iou = float(self.iouscale.get()) / 100
            batch_size = int(self.batchsz_entry.get())
            img_size = int(self.imgsz_entry.get())
            device = "cpu" if self.selected_device.get() == "CPU" else "0"
            if self.model_file_path and self.datasetfile_path and img_size and batch_size:
                self.validate.configure(state="disabled")                
                self.result_entry.insert(tk.END, "Training will Start Now...\n")
                command = [sys.executable, "-c", f"""
import subprocess
from ultralytics import YOLO

def main():
    model_path = '{self.model_file_path}'
    data_path = '{self.datasetfile_path}'
    conf = {confidence}
    iou = {iou}
    img_size = {img_size}
    batch_size = {batch_size}
    device = '{device}'
    
    model = YOLO(model_path)
    metrics = model.val(device=device, data=data_path, conf=conf,iou=iou, imgsz=img_size, batch=batch_size)
    print(metrics.box.map)
    print(metrics.box.map50)
    print(metrics.box.map75)
    print(metrics.box.maps) 
if __name__ == '__main__':
    main()
"""]
                
                # Run the training script in a separate thread to keep the GUI responsive
                thread = threading.Thread(target=self.run_validating, args=(command,))
                thread.start()
            else:
                tk.messagebox.showwarning(title="Training", message="Please fill in all required fields.")
        except ValueError:
            tk.messagebox.showwarning(title="Training", message="Integer only.")
        except NameError:
            tk.messagebox.showwarning(title="Training", message="Please fill in all required fields.")
        except AttributeError:
            tk.messagebox.showwarning(title="Training", message="Please fill in all required fields.")

    def run_validating(self, command):
        # Clear previous output
        self.result_entry.delete("1.0", tk.END)
        
        # Open subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        
        # Read output line by line and update the GUI
        for line in iter(process.stdout.readline,""):
            self.result_entry.insert(tk.END, line)
            self.result_entry.see(tk.END)
            self.update_idletasks()  # Update the GUI to show new content
        
        # Close the process and update the GUI once more
        process.stdout.close()
        process.wait()
        self.result_entry.insert(tk.END, "\nValidation finished.\n")
        self.result_entry.see(tk.END)
        self.validate.configure(state="active")
    def update_gpu_info(self):
        try:
            # Clear previous GPU information
            self.gpu_info.configure(state="normal")
            self.gpu_info.delete("1.0", tk.END)

            # Get GPU information
            gpu_info = self.get_gpu_info()

            # Update text widget with new GPU information
            if "No GPU found" not in gpu_info:
                self.gpu_info.insert(tk.END, gpu_info)
                self.after(5000, self.update_gpu_info)  # Schedule the next update after 5 seconds
            else:
                self.gpu_info.insert(tk.END, gpu_info)
                self.gpu_info.configure(state="disabled")

        except Exception as e:
            print(f"Error updating GPU info: {e}")

    def get_gpu_info(self):
        try:
            if torch.cuda.is_available():
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
            else:
                return "No GPU found"
        except Exception as e:
            print(f"Error getting GPU info: {e}")
            return "Error fetching GPU info"
    def checkgpu(self):
        chk = torch.cuda.is_available()
        if chk == True:
            self.GPU.configure(state="active")
        else:
            self.GPU.configure(state="disabled")