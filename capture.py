import cv2
import time
from PIL import Image
import numpy as np
import os

class Capture:
    def __init__(self, camera):
        self.camera = camera
        self.running = False
        self.log_callback = None

    def set_log_callback(self, callback):
        self.log_callback = callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def start_capture(self):
        self.running = True
        folder = "frames"
        os.makedirs(folder, exist_ok=True)

        while self.running:
            ret, frame = self.camera.read()
            if ret:
                # Convert the frame to a PIL image
                pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Resize the image
                max_size = 250
                ratio = max_size / max(pil_img.size)
                new_size = tuple([int(x * ratio) for x in pil_img.size])
                resized_img = pil_img.resize(new_size, Image.LANCZOS)

                # Convert the PIL image back to an OpenCV image
                frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)

                # Save the frame as an image file
                path = f"{folder}/frame.jpg"
                cv2.imwrite(path, frame)
                self.log("📸 Frame captured.")
            else:
                self.log("Failed to capture image")

            # Wait for 2 seconds
            time.sleep(2)

    def stop_capture(self):
        self.running = False
