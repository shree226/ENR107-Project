import cv2
import torch
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

app = FastAPI()

# Load the YOLO model
model_path = "runs/detect/train24/weights/best.pt"
model = YOLO(model_path)

# Try to open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("⚠️ Warning: No webcam detected! Running in test mode.")

def generate_frames():
    while True:
        ret, frame = cap.read()

        # If no webcam, send a test image instead
        if not ret:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Black image

        # Run YOLO detection
        results = model(frame)
        annotated_frame = results[0].plot()
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

        _, buffer = cv2.imencode(".jpg", annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
def home():
    return {"message": "Surgical Tool Detection API"}
