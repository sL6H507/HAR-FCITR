from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
import requests
def fetch_and_display_image(parent, url, x, y,w,h):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image = image.resize((w, h))  # Adjust size as needed
        photo = ImageTk.PhotoImage(image)
        parent.canvas.create_image(x, y, image=photo, anchor=tk.CENTER)
        parent.canvas.image = photo  # Keep a reference to prevent garbage collection
        return photo
    else:
        print(f"Failed to fetch image from URL: {url}")
        return None
    
def fetch_image(parent, url, width, height):
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((width, height))
            img = ImageTk.PhotoImage(img)
            return img
        else:
            print(f"Failed to fetch image from URL: {url}")
            return None