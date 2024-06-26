import cv2
import time
from PIL import Image
import numpy as np
import os

class Capture:
    def __init__(self, camera):
        self.folder = "frames"
        self.frames_dir = os.path.join(os.getcwd(), self.folder)
        os.makedirs(self.frames_dir, exist_ok=True)
        self.camera = camera
        self.running = False
        self.log_callback = None

    def set_log_callback(self, callback):
        self.log_callback = callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def start_capture(self):
        self.running = True
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                max_size = 250
                ratio = max_size / max(pil_img.size)
                new_size = tuple([int(x * ratio) for x in pil_img.size])
                resized_img = pil_img.resize(new_size, Image.LANCZOS)
                frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)
                path = f"{self.folder}/frame.jpg"
                cv2.imwrite(path, frame)
                self.log("📸 Say cheese! Saving frame.")
            else:
                self.log("Failed to capture image")
            time.sleep(2)

    def stop_capture(self):
        self.running = False

    def release(self):
        self.camera.release()
        cv2.destroyAllWindows()
