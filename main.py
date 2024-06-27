import tkinter as tk
from ttkbootstrap import Style, ttk
from threading import Thread
import capture as capture_module
import cv2
from PIL import Image, ImageTk
import os
import sys
from narrator import Narrator  # Import the Narrator class

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("David Attenborough Narrator")

        # Initialize ttkbootstrap style
        self.style = Style(theme='darkly')  # Use the 'darkly' theme for dark mode

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise IOError("Cannot open webcam")

        self.capture_instance = capture_module.Capture(self.camera)
        self.capture_instance.set_log_callback(self.log_message)

        self.left_frame = ttk.Frame(self.root, style="TFrame")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(self.root, style="TFrame")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.video_label = ttk.Label(self.left_frame, style="TLabel")
        self.video_label.pack(padx=10, pady=10)

        button_frame = ttk.Frame(self.left_frame, style="TFrame")
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Capture", command=self.start_capture, bootstyle="primary")
        self.start_button.pack(side=tk.LEFT, padx=5, pady=(0, 0))

        self.stop_button = ttk.Button(button_frame, text="Stop Capture", command=self.stop_capture, bootstyle="danger")
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=(0, 0))

        # Set a smaller font for the explanatory text
        small_font = ('Helvetica', 10)

        self.capture_explanation = ttk.Label(self.left_frame, text="Start capturing frames from the webcam.", style="TLabel", font=small_font)
        self.capture_explanation.pack(padx=10, pady=(0, 1))  # Reduce the padding between the buttons and the text

        self.log_output = tk.Text(self.left_frame, wrap=tk.WORD, state=tk.DISABLED, height=10, bg="#2E2E2E", fg="#FFFFFF")
        self.log_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        narrate_button_frame = ttk.Frame(self.right_frame, style="TFrame")
        narrate_button_frame.pack(pady=10)

        self.narrate_button = ttk.Button(narrate_button_frame, text="Start Narrating", command=self.start_narrating, bootstyle="primary")
        self.narrate_button.pack(side=tk.LEFT, padx=5, pady=(0, 0))

        self.stop_narrate_button = ttk.Button(narrate_button_frame, text="Stop Narrating", command=self.stop_narrating, bootstyle="danger")
        self.stop_narrate_button.pack(side=tk.LEFT, padx=5, pady=(0, 0))

        self.narrate_explanation = ttk.Label(self.right_frame, text="Start narrating the captured frames.", style="TLabel", font=small_font)
        self.narrate_explanation.pack(padx=10, pady=(0, 1))  # Reduce the padding between the buttons and the text

        self.narration_output = tk.Text(self.right_frame, wrap=tk.WORD, state=tk.DISABLED, height=10, bg="#2E2E2E", fg="#FFFFFF")
        self.narration_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.capture_thread = None  # Initialize capture_thread
        self.narration_thread = None  # Initialize narration_thread
        self.narrator = None  # Narrator instance
        self.update_video_feed()  # Start updating the video feed

    def log_message(self, message):
        self.log_output.configure(state=tk.NORMAL)
        self.log_output.insert(tk.END, message + '\n')
        self.log_output.configure(state=tk.DISABLED)
        self.log_output.see(tk.END)

    def update_narration_output(self, message):
        self.narration_output.configure(state=tk.NORMAL)
        self.narration_output.insert(tk.END, message + '\n')
        self.narration_output.configure(state=tk.DISABLED)
        self.narration_output.see(tk.END)

    def start_capture(self):
        if self.capture_thread is None or not self.capture_thread.is_alive():
            self.capture_thread = Thread(target=self.capture_instance.start_capture)
            self.capture_thread.start()

    def stop_capture(self):
        if self.capture_instance:
            self.capture_instance.stop_capture()
            if self.capture_thread:
                self.capture_thread.join()
            self.log_message("🛑 Stopped capturing.")

    def update_video_feed(self):
        ret, frame = self.camera.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            img = img.resize((320, 240), Image.LANCZOS)  # Resize the image to make it smaller
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.configure(image=imgtk)
            self.video_label.image = imgtk  # Store the image to avoid garbage collection
        self.root.after(20, self.update_video_feed)  # Schedule the next update

    def start_narrating(self):
        if self.narration_thread is None or not self.narration_thread.is_alive():
            self.narration_thread = Thread(target=self.run_narrator)
            self.narration_thread.start()

    def stop_narrating(self):
        if self.narrator:
            self.narrator.stop_narration()
            self.update_narration_output("🛑 Stopped narrating.")

    def run_narrator(self):
        self.narrator = Narrator()
        self.narrator.set_log_callback(self.update_narration_output)
        self.narrator.start_narration()

    def on_closing(self):
        self.stop_capture()
        self.stop_narrating()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
