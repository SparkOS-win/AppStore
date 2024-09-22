import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from urllib.parse import urlsplit
import json
import threading

def load_apps():
    json_path = r'C:\Windows\SparkModules\AppStoreData\apps.json'
    with open(json_path, 'r') as file:
        return json.load(file)

def download_app(url, name, progress_label, progress_bar):
    try:
        file_name = os.path.basename(urlsplit(url).path)
        file_path = os.path.join(os.getcwd(), file_name)

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        downloaded_size = 0
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_percentage = int(downloaded_size / total_size * 100)
                    progress_bar['value'] = progress_percentage
                    progress_label.config(text=f"Downloading {name}: {progress_percentage}%")
                    progress_bar.update()

        messagebox.showinfo("Download Complete", f"{name} has been downloaded!")
        os.startfile(file_path)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download {name}: {str(e)}")
    finally:
        progress_label.config(text="")
        progress_bar['value'] = 0

def start_download(url, name, progress_label, progress_bar):
    threading.Thread(target=download_app, args=(url, name, progress_label, progress_bar)).start()

def create_app_buttons(apps, frame, progress_label, progress_bar):
    for app in apps:
        app_frame = tk.Frame(frame, bg="#2c2c2c", bd=2, relief="ridge", padx=10, pady=10)
        app_frame.pack(fill="x", padx=50, pady=5)  # Add horizontal padding to center

        name_label = tk.Label(app_frame, text=app['name'], font=("Arial", 14, "bold"), fg="#ffffff", bg="#2c2c2c")
        name_label.pack(side="top", anchor="w")

        desc_label = tk.Label(app_frame, text=app['description'], font=("Arial", 10), fg="#cccccc", bg="#2c2c2c")
        desc_label.pack(side="top", anchor="w")

        install_button = tk.Button(app_frame, text="Install", width=10, bg="#1e1e1e", fg="#ffffff",
                                   command=lambda url=app['url'], name=app['name']: start_download(url, name, progress_label, progress_bar))
        install_button.pack(side="right")

def create_app_store():
    window = tk.Tk()
    window.title("SparkOS App Store")
    window.geometry("600x800")
    window.config(bg="#1e1e1e")

    frame = tk.Frame(window, bg="#1e1e1e")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="#1e1e1e", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    progress_frame = tk.Frame(window, bg="#1e1e1e", padx=10, pady=10)
    progress_frame.pack(fill="x", side="bottom")

    progress_label = tk.Label(progress_frame, text="", font=("Arial", 10), fg="#ffffff", bg="#1e1e1e")
    progress_label.pack(side="top", anchor="w")

    progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
    progress_bar.pack(side="top", fill="x", padx=10, pady=10)

    apps = load_apps()
    create_app_buttons(apps, scrollable_frame, progress_label, progress_bar)

    window.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    window.mainloop()

create_app_store()
