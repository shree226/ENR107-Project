import streamlit as st
import torch
from ultralytics import YOLO
import numpy as np
import cv2
import os

# Streamlit Title
st.title("Surgical Tool Detection in Real-time")

# Load the YOLO model
model_path = os.path.join("runs", "detect", "train24", "weights", "best.pt")

if not os.path.exists(model_path):
    st.error(f"Model file not found at {model_path}. Please check your file path.")
else:
    model = YOLO(model_path)

# Placeholder for video feed
stframe = st.empty()

# Function to start webcam
def run_detection():
    cap = cv2.VideoCapture(0)  # Use the default webcam
    cap.set(3, 640)  # Set width
    cap.set(4, 480)  # Set height

    if not cap.isOpened():
        st.error("Could not open webcam. Please allow access and restart.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video. Check your camera permissions.")
            break

        # Run YOLO model on the frame
        results = model(frame)

        # Draw detections
        annotated_frame = results[0].plot()
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

        # Display the video in the Streamlit app
        stframe.image(annotated_frame, channels="RGB", use_column_width=True)

        # Stop the loop when the user clicks "Stop Detection"
        if st.button("Stop Detection"):
            break

    cap.release()
    st.write("Detection stopped. Restart to continue.")

# User selects an option
option = st.radio("Choose an option:", ["Start Detection", "Stop Detection", "Settings"])

if option == "Start Detection":
    run_detection()

elif option == "Stop Detection":
    st.write("Detection stopped. Restart to continue.")

elif option == "Settings":
    st.write("Adjust detection settings here.")
