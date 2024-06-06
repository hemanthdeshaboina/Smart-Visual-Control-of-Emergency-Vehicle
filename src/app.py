from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import webbrowser
from flask_ngrok import run_with_ngrok
import numpy
from playsound import playsound

app = Flask(__name__)
run_with_ngrok(app)
# Load the YOLO model from a specified checkpoint file
model = YOLO("last (1).pt")
confidence_threshold=0.3
# Global variable to store ambulance detection status
ambulance_detected = False

def detect_objects(frame):
    global ambulance_detected
    
    # Perform object detection
    results = model(frame)[0]
    
    # Check if an ambulance is detected
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > confidence_threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            label = results.names[int(class_id)].upper()
            if label == "AMBULANCE":
                ambulance_detected = True
                 # Play the sound file
                
            else:
                ambulance_detected = False
            
    # Draw bounding boxes and labels on the frame
    

    return frame

def generate_frames():
    cap = cv2.VideoCapture(1)  # Use 0 for default webcam source

    while True:
        success, frame = cap.read()

        if not success:
            break

        # Detect objects in the frame
        frame = detect_objects(frame)
       

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)

        if not ret:
            break

        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        
        

@app.route('/')
def index():
    global ambulance_detected 
    status_message = True if ambulance_detected else False
    ambulance_detected=False
    return render_template('index2.html', status_message=status_message)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


    

if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()
