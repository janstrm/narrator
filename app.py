import os
import sys
import contextlib
import logging
import webbrowser

# Suppress Pygame initialization messages
with open(os.devnull, 'w') as fnull:
    with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
        import pygame

from flask import Flask, render_template, request, jsonify, Response
import capture as capture_module
import cv2
from narrator import Narrator
from threading import Thread
import signal

app = Flask(__name__)

# Suppress HTTP request logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Initialize the camera
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise IOError("Cannot open webcam")

capture_instance = capture_module.Capture(camera)
narrator_instance = Narrator()

capture_log_messages = []
narration_log_messages = []

def add_capture_log_message(message):
    capture_log_messages.append(message)
    if len(capture_log_messages) > 100:  # Keep only the last 100 messages
        capture_log_messages.pop(0)

def add_narration_log_message(message):
    narration_log_messages.append(message)
    if len(narration_log_messages) > 100:  # Keep only the last 100 messages
        narration_log_messages.pop(0)

capture_instance.set_log_callback(add_capture_log_message)
narrator_instance.set_log_callback(add_narration_log_message)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    if not capture_instance.running:
        Thread(target=capture_instance.start_capture).start()
        add_capture_log_message('📸 Capture started.')
    return jsonify({'status': 'started'})

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    capture_instance.stop_capture()
    add_capture_log_message('🛑 Capture stopped.')
    return jsonify({'status': 'stopped'})

@app.route('/start_narrating', methods=['POST'])
def start_narrating():
    if not narrator_instance.running:
        Thread(target=narrator_instance.start_narration).start()
        add_narration_log_message('Narration started.')
    return jsonify({'status': 'started'})

@app.route('/stop_narrating', methods=['POST'])
def stop_narrating():
    narrator_instance.stop_narration()
    add_narration_log_message('Narration stopped.')
    return jsonify({'status': 'stopped'})

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({'capture': capture_log_messages, 'narration': narration_log_messages})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
    print(f"Starting Flask server at {url}")
    webbrowser.open(url)
    app.run(debug=False)
