import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox
from typing import Callable
import yt_dlp
import os


# -------------------------------------------------
# Download-Funktion (aus deinem Originalcode)
# -------------------------------------------------

def download_youtube_as_mp3(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'prefer_ffmpeg': True,
        'noplaylist': True,
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🎧 Downloading and converting: {url}")
        ydl.download([url])
        print("✅ Conversion complete!")


# -------------------------------------------------
# GUI
# -------------------------------------------------

class GUI:
    
    def __init__(self):
        self._gui_config()
        
        
    def _gui_config(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("450x260")
        self.root.title("YouTube → MP3 Converter")

        # --- Input field ---
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.root, textvariable=self.input_var, font=("Arial", 14), width=35)
        self.input_entry.place(relx=0.5, y=60, anchor="n")

        # --- Buttons ---
        create_button(self, "btn_choose", "Choose File", self.on_choose_file, 0.5, 110)
        create_button(self, "btn_convert", "Convert", self.on_convert, 0.5, 160)


    # -----------------------
    #  Button callbacks
    # -----------------------

    def on_choose_file(self):
        file = filedialog.askopenfilename(
            title="Select .txt file",
            filetypes=[("Text files", "*.txt")]
        )
        if file:
            self.input_var.set(file)
            print("File chosen:", file)


    def on_convert(self):
        txt_path = self.input_var.get()

        if not txt_path or not os.path.isfile(txt_path):
            messagebox.showerror("Error", "Please choose a valid .txt file first!")
            return

        # Ordner zum Speichern auswählen
        output_folder = filedialog.askdirectory(title="Select output folder")

        if not output_folder:
            return

        # TXT Datei laden
        with open(txt_path, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f.readlines() if line.strip()]

        if not links:
            messagebox.showerror("Error", "The selected file contains no YouTube links.")
            return

        # Jeden Link konvertieren
        for url in links:
            try:
                download_youtube_as_mp3(url, output_folder)
            except Exception as e:
                print(f"❌ Error with {url}: {e}")

        messagebox.showinfo("Done", "All downloads completed!")


# -------------------------------------------------
# Helper methods
# -------------------------------------------------

def create_button(self, name_Button: str, text: str, command: Callable[[], None], x: float, y: int) -> None:
    button = Button(self.root, text=text, width=14, font=("Arial", 14), command=command)
    button.place(relx=x, y=y, anchor="n")
    setattr(self, name_Button, button)


def create_label(root, text, relx: float, y: int, size) -> None:    
    text_var = tk.StringVar(value=text)
    label = Label(root, textvariable=text_var, font=("Arial", size, "bold"))
    label.place(relx=relx, y=y, anchor="n")

