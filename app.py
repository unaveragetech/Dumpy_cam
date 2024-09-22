import cv2
from flask import Flask, render_template, Response, redirect, url_for
import os
import sys
import subprocess
from imageio import get_writer
from PIL import Image
import time
from pyngrok import ngrok

ngrok_auth_token = "your token here"


app = Flask(__name__)

# Camera control
camera_index = 0
camera = None
is_camera_on = False
output_directory = "media_output"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def check_dependencies():
    # Automatically install missing dependencies
    required = ['opencv-python', 'flask', 'imageio', 'Pillow', 'pyngrok']
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *required])
        print("All dependencies installed. Restarting the script.")
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Failed to install dependencies: {e}")

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

# Switch between cameras
@app.route('/switch_camera/<int:new_index>')
def switch_camera(new_index):
    global camera_index, camera
    camera_index = new_index
    if camera:
        camera.release()
    camera = cv2.VideoCapture(camera_index)
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

# Save frames as pictures
@app.route('/save_picture')
def save_picture():
    if camera and is_camera_on:
        success, frame = camera.read()
        if success:
            img_path = f"{output_directory}/img_{time.time()}.jpg"
            cv2.imwrite(img_path, frame)
            return f"Image saved to {img_path}"
    return "Camera is not on."

# Save video as GIF
@app.route('/save_gif')
def save_gif():
    gif_path = f"{output_directory}/output_{time.time()}.gif"
    with get_writer(gif_path, mode='I') as writer:
        for _ in range(30):  # Save 30 frames
            success, frame = camera.read()
            if success:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                writer.append_data(image)
            else:
                break
    return f"GIF saved to {gif_path}"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    check_dependencies()
    
    # Start the ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f"Ngrok Tunnel URL: {public_url}")
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
