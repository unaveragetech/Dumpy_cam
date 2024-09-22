import cv2
from flask import Flask, render_template, Response, redirect, url_for
import os
import subprocess
import sys
import pkg_resources
from imageio import get_writer
from PIL import Image
import time
from pyngrok import ngrok

ngrok_auth_token = "your token here"  # Replace with your actual token

app = Flask(__name__)

# Camera control
camera_index = 0
camera = None
is_camera_on = False
output_directory = "media_output"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def check_dependencies():
    required = ['opencv-python', 'flask', 'imageio', 'Pillow', 'pyngrok']
    installed = {pkg.key for pkg in pkg_resources.working_set}

    missing = [pkg for pkg in required if pkg not in installed]
    
    if missing:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
            print(f"Installed missing dependencies: {', '.join(missing)}.")
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
    else:
        print("All required dependencies are already installed.")

# Toggle camera on/off
def toggle_camera(state):
    global camera, is_camera_on
    if state == 'on':
        if not is_camera_on:
            camera = cv2.VideoCapture(camera_index)
            is_camera_on = True
    elif state == 'off':
        if camera:
            camera.release()
        is_camera_on = False

@app.route('/toggle/<state>')
def toggle(state):
    toggle_camera(state)
    return redirect(url_for('index'))

# Stream the camera feed
def generate_feed():
    while is_camera_on and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    check_dependencies()

    # Set the ngrok auth token and start the tunnel
    ngrok.set_auth_token(ngrok_auth_token)
    public_url = ngrok.connect(5000)
    print(f"Ngrok Tunnel URL: {public_url}")

    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
