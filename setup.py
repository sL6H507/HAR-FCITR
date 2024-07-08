import subprocess
import sys
import tkinter as tk
from tkinter import Canvas, messagebox

class Setup(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        check_button = tk.Button(self, text="Check Required Packages", command=self.check_packages)
        check_button.pack(pady=20)
        self.canvas.place(x=0, y=0)

    def get_requirements(self):
        return [
            'absl-py==2.1.0', 'aiofiles==23.2.1', 'altgraph==0.17.4', 'anyio==4.3.0', 
            'argcomplete==3.3.0', 'attrs==23.2.0', 'beautifulsoup4==4.12.3', 'bleach==6.1.0', 
            'boto3==1.34.101', 'botocore==1.34.101', 'brotli==1.1.0', 'cachetools==5.3.3', 
            'cython==3.0.10', 'dacite==1.7.0', 'defusedxml==0.7.1', 'deprecated==1.2.14', 
            'dill==0.3.8', 'dnspython==2.6.1', 'fastjsonschema==2.19.1', 'fiftyone==0.23.8', 
            'fiftyone-brain==0.16.1', 'fiftyone-db==1.1.2', 'fiftyone-desktop==0.33.7', 
            'ftfy==6.2.0', 'future==1.0.0', 'glob2==0.7', 'graphql-core==3.2.3', 'grpcio==1.63.0', 
            'h11==0.14.0', 'h2==4.1.0', 'hpack==4.0.0', 'httpcore==1.0.5', 'httpx==0.27.0', 
            'humanize==4.9.0', 'hypercorn==0.16.0', 'hyperframe==6.0.1', 'imageio==2.34.1', 
            'inflate64==1.0.0', 'jmespath==1.0.1', 'joblib==1.4.2', 'jsonlines==4.0.0', 
            'jupyterlab-pygments==0.3.0', 'kaleido==0.2.1', 'lapx==0.5.9', 'lazy-loader==0.4', 
            'markdown==3.6', 'mistune==3.0.2', 'mongoengine==0.24.2', 'motor==3.4.0', 
            'multivolumefile==0.2.3', 'nbclient==0.10.0', 'nbconvert==7.16.4', 'nbformat==5.10.4', 
            'opencv-python==4.9.0.80', 'pafy==0.5.5', 'pandas==2.2.2', 'pandocfilters==1.5.1', 
            'pefile==2023.2.7', 'pickleshare==0.7.5', 'plotly==5.22.0', 'pprintpp==0.4.0', 
            'priority==2.0.0', 'protobuf==5.26.1', 'py7zr==0.21.0', 'pybcj==1.0.2', 'pycocotools==2.0', 
            'pycryptodomex==3.20.0', 'pyinstaller==6.6.0', 'pyinstaller-hooks-contrib==2024.6', 
            'pymongo==4.7.2', 'pyppmd==1.1.0', 'pywin32-ctypes==0.2.2', 'pyzstd==0.15.10', 
            'rarfile==4.2', 'regex==2024.4.28', 'retrying==1.3.4', 's3transfer==0.10.1', 
            'scikit-image==0.23.2', 'scikit-learn==1.4.2', 'sniffio==1.3.1', 'sortedcontainers==2.4.0', 
            'soupsieve==2.5', 'sse-starlette==0.10.3', 'sseclient-py==1.8.0', 'starlette==0.37.2', 
            'strawberry-graphql==0.138.1', 'tabulate==0.9.0', 'tenacity==8.3.0', 'tensorboard==2.16.2', 
            'tensorboard-data-server==0.7.2', 'texttable==1.7.0', 'threadpoolctl==3.5.0', 'tifffile==2024.5.3', 
            'tinycss2==1.3.0', 'torchaudio==2.3.0', 'torchvision==0.18.0', 'tzlocal==5.2', 
            'universal-analytics-python3==1.1.1', 'voxel51-eta==0.12.6', 'wcwidth==0.2.13', 
            'webencodings==0.5.1', 'werkzeug==3.0.3', 'wrapt==1.16.0', 'wsproto==1.2.0', 'xmltodict==0.13.0', 
            'youtube-dl==2020.12.2'
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
            messagebox.showinfo("Result", "All required packages are installed.")
        else:
            result = "The following packages are missing:\n" + "\n".join(missing_packages)
            messagebox.showwarning("Result", result)
            self.install_packages(missing_packages)
            messagebox.showinfo("Result", "Missing packages have been installed.")
            self.quit()  # Close the setup window after checking/installing packages

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x480")
    app = Setup(root)
    app.pack(fill="both", expand=True)
    root.mainloop()