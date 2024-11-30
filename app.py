from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
import datetime
import time  # For time-based control of sound alerts
import pygame  # For playing beep sound

app = Flask(__name__)

# Initialize complaints log
complaints_log = []

# Load the YOLO model
class_name = []
with open(os.path.join("project_files", 'obj.names'), 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

net1 = cv2.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
net1.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)  # Use OpenCV backend
net1.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)       # Use CPU for processing
model1 = cv2.dnn_DetectionModel(net1)
model1.setInputParams(size=(640, 480), scale=1 / 255, swapRB=True)

# Initialize pygame mixer for playing sound
pygame.mixer.init()
BEEP_FILE_PATH = os.path.join("static", "beep.mp3")

# Function to play a beep sound
def play_beep():
    try:
        pygame.mixer.music.load(BEEP_FILE_PATH)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing beep sound: {e}")

# Function to log a complaint
def log_complaint(location="User Defined Location"):
    for complaint in complaints_log:
        if complaint['location'] == location:
            return  # If a complaint already exists for this location, don't log again

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Pending"

    complaints_log.append({
        'location': location,
        'timestamp': timestamp,
        'status': status
    })

    with open("project_files/complaints.txt", "a") as f:
        f.write(f"Location: {location}, Time: {timestamp}, Status: {status}\n")

# Video processing generator
def generate_frames(video_path=None):
    Conf_threshold = 0.5
    NMS_threshold = 0.4
    min_pothole_size = 5000  # Threshold for pothole size (area in pixels)
    beep_delay = 3  # Minimum time (in seconds) between consecutive beeps
    last_beep_time = 0  # Track the last time a beep was played

    cap = cv2.VideoCapture(0 if video_path is None else video_path)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Detect objects in the frame
        classes, scores, boxes = model1.detect(frame, Conf_threshold, NMS_threshold)
        current_time = time.time()
        pothole_detected = False

        for (classid, score, box) in zip(classes, scores, boxes):
            label = "pothole"
            if score >= 0.7:  # Confidence threshold for pothole detection
                x, y, w, h = box
                area = w * h  # Calculate the area of the detected pothole
                if area >= min_pothole_size:  # Check if pothole size is large enough
                    pothole_detected = True
                    # Draw the bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {int(score * 100)}%", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Play a beep sound only if a pothole is detected and the delay has passed
        if pothole_detected and (current_time - last_beep_time >= beep_delay):
            play_beep()
            last_beep_time = current_time

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No file uploaded", 400

    video_file = request.files['video']
    video_path = os.path.join("project_files", video_file.filename)
    video_file.save(video_path)

    return Response(generate_frames(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam')
def webcam_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        user_ip = request.remote_addr
        log_complaint(location=user_ip)
        return redirect(url_for('complaints'))

    return render_template('complaints.html', complaints=complaints_log)

if __name__ == '__main__':
    app.run(debug=True)
