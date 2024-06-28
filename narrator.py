import os
import openai
import base64
import time
import simpleaudio as sa
import errno
from elevenlabs import generate, play, set_api_key, voices
import pygame
from dotenv import load_dotenv
import sys
import contextlib

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set your ElevenLabs API key
set_api_key(os.getenv('ELEVENLABS_API_KEY'))
voiceID = os.getenv('ELEVENLABS_VOICE_ID')

class Narrator:
    def __init__(self):
        self.running = False
        self.log_callback = None

    def set_log_callback(self, callback):
        self.log_callback = callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def encode_image(self, image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    raise
                time.sleep(0.1)

    def play_audio(self, text):
        audio = generate(text, voice=voiceID)

        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        # Temporarily suppress stdout and stderr to hide Pygame initialization messages
        with open(os.devnull, 'w') as fnull:
            with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                pygame.init()
                pygame.mixer.init()

        try:
            sound = pygame.mixer.Sound(file=file_path)
            sound.play()

            while pygame.mixer.get_busy():
                pygame.time.Clock().tick(10)

        except pygame.error as e:
            self.log(f"Error playing audio: {str(e)}")

        pygame.mixer.quit()
        pygame.quit()

    def generate_new_line(self, base64_image):
        return {
            "role": "user",
            "content": f"Describe this image: data:image/jpeg;base64,{base64_image}"
        }

    def analyze_image(self, base64_image, script):
        messages = [
            {"role": "system", "content": """
                You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                Make it snarky and very funny, include meme references if it fits. Don't repeat yourself. Max 120 words output. Make it short. If the human does do anything remotely interesting, make a big deal about it!
                """
            },
            *script,
            self.generate_new_line(base64_image)
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
        )

        response_text = response.choices[0].message.content
        return response_text

    def start_narration(self):
        self.running = True
        script = []

        while self.running:
            image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

            base64_image = self.encode_image(image_path)

            self.log("👀 David is watching...")
            analysis = self.analyze_image(base64_image, script=script)

            self.log("🎙️ David says:")
            self.log(analysis)

            self.play_audio(analysis)

            script.append({"role": "assistant", "content": analysis})

            time.sleep(5)

    def stop_narration(self):
        self.running = False
        self.log("Narration stopped.")

if __name__ == "__main__":
    narrator = Narrator()
    narrator.start_narration()
