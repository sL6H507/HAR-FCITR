import subprocess
import sys
import tkinter as tk
from tkinter import Canvas, Label, messagebox

class Setup(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="#FFFFFF", width=300, height=200)
        
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=300,
            width=200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        button_1 = tk.Button(self, text="Check Required Packages", command=self.check_packages, font=("Inter", 10), relief="flat")
        button_1.place(relx=0.5, rely=0.6, anchor=tk.CENTER, width=200, height=50)

        welcome_label = Label(self, text="Welcome To Our Project\n", font=("Inter", 12),bg="#ffffff")
        welcome_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def get_requirements(self):
        return [
            "mysql-connector-python",
            "Pillow",
            "requests",
            "opencv-python",
            "ultralytics",
            "roboflow",
            "nvsmi",
            "tensorflow",
            "tensorboard",
            "torch",
            "torchvision",
            "torchaudio"
        ]

    def check_installed_packages(self, requirements):
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format', 'freeze'], 
                                    stdout=subprocess.PIPE, text=True)
            installed_packages = result.stdout.lower().splitlines()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to get installed packages\n{str(e)}")
            return []

        missing = []
        for req in requirements:
            pkg_name = req.split('==')[0].lower()
            if not any(pkg_name in installed_pkg for installed_pkg in installed_packages):
                missing.append(req)
        return missing

    def install_packages(self, packages):
        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to install {package}\n{str(e)}")

    def check_packages(self):
        requirements = self.get_requirements()
        if not requirements:
            return
        missing_packages = self.check_installed_packages(requirements)
        
        if not missing_packages:
            messagebox.showinfo("Result", "All required packages are installed.\nFor GPU install Cuda toolkit first")
            self.quit()
        else:
            result = "The following packages are missing:\n" + "\n".join(missing_packages)
            messagebox.showwarning("Result", result)
            self.install_packages(missing_packages)
            messagebox.showinfo("Result", "Missing packages have been installed.\nFor GPU install Cuda toolkit first")
            self.quit()

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")
    root.resizable(False, False)    
    app = Setup(root)
    app.pack(fill="both", expand=False)
    
    center_window(root, 300, 200)
    
    root.mainloop()
