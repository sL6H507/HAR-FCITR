import tkinter as tk
from tkinter import Canvas, Button, filedialog, OptionMenu, Text, Radiobutton, messagebox
from utils import fetch_image,fetch_and_display_image
import threading,subprocess,sys,home,predict,torch,nvsmi,os,yaml
from ultralytics import YOLO
from roboflow import Roboflow

class Train(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selected_device = tk.StringVar()
        self.selected_device.set(None)
        self.value_model_inside = tk.StringVar(self) 
        self.value_dataset_inside = tk.StringVar(self)
        self.rf = Roboflow(api_key="HFgIJHLGYqUPmOtgYZ1m")
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

        self.canvas.create_text(316.0, 147.0, anchor="nw", text="Select Pre-Trained Model", fill="#000000",
                                font=("Inter", 32 * -1))
        
        self.image_image_1 = fetch_and_display_image(self,"https://media.tenor.com/Q8nIjfXA_awAAAAi/fcitr.gif", 115.0, 107.0,214,209)

        predict_page_btn = tk.Button(self, text="Predicting", font=("Inter", 15),justify="left", borderwidth=0, highlightthickness=0,bg="#FFFFFF",
                                     command=lambda: controller.show_frame_with_auth(predict.Predict), relief="flat")
        predict_page_btn.place(x=25.0, y=911.0, width=259.0, height=82.0)

        self.Training_btn = tk.Button(self, text="Train", font=("Inter", 20), borderwidth=0, highlightthickness=0,
                                      command=self.start_training, relief="flat")
        self.Training_btn.place(x=659.0, y=448.0, width=148.0, height=39.0)

        #self.entry_1 = tk.Entry(self, bd=0, bg="#F8F8F8", fg="#000716", highlightthickness=0)
        #self.entry_1.place(x=316.0, y=384.0, width=502.0, height=43.0)
        self.canvas.create_text(316.0, 341.0, anchor="nw", text="Select The Dataset (.yaml):", fill="#000000",
                                font=("Inter", 32 * -1))
        self.value_dataset_inside.set("Select Dataset") 
        options_dataset_list = ["Human Action Recognition", "Other"] 

        dataset_menu = tk.OptionMenu(self, self.value_dataset_inside, *options_dataset_list, command=self.change_dataset) 
        dataset_menu.place(x=405.0, y=380.0, width=189.0, height=49.0)
        #self.button_image_3 = fetch_image(self,"https://media.tenor.com/kEvgsQa811YAAAAM/dir.gif", 70, 36)
        #datafile_btn = tk.Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0,command=self.select_data_file, relief="flat")
        #datafile_btn.place(x=818.0, y=384.0, width=70.0, height=45.0)

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

        self.value_model_inside.set("Select a Pre-Trained Model") 
        options_model_list = ["YoloV9 Compact", "YoloV9 Extended", "Gelan Compact", "Gelan Extended","Other"] 

        model_menu = tk.OptionMenu(self, self.value_model_inside, *options_model_list, command=self.change_model) 
        model_menu.place(x=405.0, y=227.0, width=189.0, height=49.0)

        TensorBoard_btn = tk.Button(self, text="TensorBoard", font=("Inter", 20), borderwidth=0, highlightthickness=0,
                                    command=self.start_tensorboard, relief="flat")
        TensorBoard_btn.place(x=578.0, y=911.0, width=259.0, height=82.0)

        self.GPU = tk.Radiobutton(
            self,
            text="GPU",
            borderwidth=0,
            highlightthickness=0,
            variable=self.selected_device,
            value="GPU",
            relief="flat",
            )
        self.GPU.place(x=913.0, y=385.0, width=100.0, height=44.0)

        self.CPU = tk.Radiobutton(
            self,
            text="CPU",
            borderwidth=0,
            highlightthickness=0,
            variable=self.selected_device,
            value="CPU",
            relief="flat"
        )
        self.CPU.place(x=1025.0, y=385.0, width=100.0, height=44.0)
        
        self.canvas.create_text(913.0, 341.0, anchor="nw", text="Train Using :", fill="#000000",
                                font=("Inter", 36 * -1))
        self.homepage_btn = tk.Button(self, text="Home Page", font=("Inter", 15), bg="#FFFFFF", 
                                      command=lambda: controller.show_frame_with_auth(home.HomePage), borderwidth=0,
                                      highlightthickness=0, relief="flat")
        self.homepage_btn.place(x=1276, y=921, width=131, height=50)
        self.checkgpu()
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
            return self.data_file_path
    
    def select_logdir_file(self):
        self.logdir_file = filedialog.askdirectory(
            title="Select Log Directory"
        )        
        return self.logdir_file

    def change_model(self, selection):
        if selection == "Other":
            self.select_model_file()
        else:
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

    def change_dataset(self, selection):
        if selection == "Other":
            self.select_data_file()
        else:
            if selection == "Human Action Recognition":
                try:
                    project = self.rf.workspace("realtime-human-action-recognition-in-still-images-c4ciq").project("real-time-human-action-recognition")
                    version = project.version(7)
                    dataset = version.download("yolov9")
                    print(dataset.model_format)
                    self.data_file_path = os.path.join(dataset.location, "data.yaml")                     
                    self.reorganize_data_yaml(self.data_file_path)
                    self.data_file_path = self.data_file_path.replace("\\", "/")
                    print(self.data_file_path)
                except Exception as e:
                    tk.messagebox.showerror(title="Dataset Error", message=f"An error occurred: {e}")
            else:
                self.data_file_path = None
                tk.messagebox.showwarning(title="Training", message="Wrong Selection")

    def reorganize_data_yaml(self,file_path):
        with open(file_path, 'r') as file:
            existing_data = yaml.safe_load(file)
        updated_data = {
            'train': '../train/images',
            'val': '../valid/images',
            'test': '../test/images',
            'nc': existing_data['nc'],
            'names': existing_data['names']
        }
        with open(file_path, 'w') as file:
            yaml.safe_dump(updated_data, file, default_flow_style=False)

        print(f"data.yaml updated with reorganized structure at: {file_path}")

    def start_training(self):
        try:
            epochs = int(self.epochs_field.get())
            batch_size = int(self.batchsz_field.get())
            img_size = int(self.imgsz_field.get())
            device = "cpu" if self.selected_device.get() == "CPU" else "0"
            if self.trainmodel_file_path and self.data_file_path and epochs and img_size and batch_size:
                self.Training_btn.configure(state="disabled")                
                self.entry_2.insert(tk.END, "Training will Start Now...\n")
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
        for line in iter(process.stdout.readline,""):
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
        try:
            # Clear previous GPU information
            self.gpu_info.delete("1.0", tk.END)

            # Get GPU information
            gpu_info = self.get_gpu_info()

            # Update text widget with new GPU information
            self.gpu_info.insert(tk.END, gpu_info)
        except Exception as e:
            print(f"Error updating GPU info: {e}")

        # Schedule the next update after 5 seconds (5000 milliseconds)
        self.after(5000, self.update_gpu_info)

    def get_gpu_info(self):
        try:
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
        except Exception as e:
            print(f"Error getting GPU info: {e}")
            return "Error fetching GPU info"
    
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
    def checkgpu(self):
        chk = torch.cuda.is_available()
        if chk == True:
            self.GPU.configure(state="active")
        else:
            self.GPU.configure(state="disabled")
            
