import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access the webcam.")
else:
    print("Webcam is ready.")

cap.release()
