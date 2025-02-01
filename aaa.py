from flask import Flask, request, jsonify
import os
import cv2
import numpy as np

app = Flask(__name__)

# Create a directory to save images
SAVE_DIR = "saved_images"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    try:
        # Get image from request
        file = request.files["frame"]
        filename = os.path.join(SAVE_DIR, f"frame_{len(os.listdir(SAVE_DIR))}.jpg")

        # Read the image and save
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite(filename, image)

        return jsonify({"message": "Frame saved", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
