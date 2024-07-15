import subprocess,sys,os
import tkinter as tk
from tkinter import Canvas, Label, messagebox

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

        welcome_label = Label(text="Welcome To Our Project", font=("Inter", 12), bg="#FFFFFF")
        welcome_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def check_installed_packages(self, requirements_file):
        try:
            with open(requirements_file, 'r') as f:
                requirements = f.readlines()
                requirements = [req.strip() for req in requirements if req.strip()]

            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format', 'freeze'], 
                                    stdout=subprocess.PIPE, text=True)
            installed_packages = result.stdout.lower().splitlines()
            
            installed_packages_lower = [pkg.lower() for pkg in installed_packages]
            missing = []
            for req in requirements:
                pkg_name = req.split('==')[0].lower()
                if not any(pkg_name in installed_pkg for installed_pkg in installed_packages_lower):
                    missing.append(req)
            return missing

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to get installed packages\n{str(e)}")
            return []
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{requirements_file}' not found.")
            return []

    def install_packages(self, requirements_file):
        try:
            with open(requirements_file, 'r') as f:
                requirements = f.readlines()
                requirements = [req.strip() for req in requirements if req.strip()]

            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file,'--no-warn-script-location'])
            print("Successfully installed all dependencies from requirements.txt.")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install packages from {requirements_file}\n{str(e)}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{requirements_file}' not found.")

    def check_packages(self):
        requirements_file = "requirements.txt"  # Specify your requirements.txt file
        missing_packages = self.check_installed_packages(requirements_file)
        
        if not missing_packages:
            messagebox.showinfo("Result", "All required packages are already installed.")
            return
        
        result = "The following packages are missing:\n" + "\n".join(missing_packages)
        messagebox.showwarning("Result", result)
        
        self.install_packages(requirements_file)
        messagebox.showinfo("Result", "Missing packages have been installed.")
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
