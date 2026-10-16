"""Flask server for the real-time age and gender detector."""
from __future__ import annotations

import os
from functools import lru_cache

import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request, send_file

from detector import AgeGenderDetector, ModelUnavailableError

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024


@lru_cache(maxsize=1)
def get_detector() -> AgeGenderDetector:
    return AgeGenderDetector()


def decode_upload() -> np.ndarray | None:
    upload = request.files.get("image")
    if upload is None or not upload.filename:
        return None
    buffer = np.frombuffer(upload.read(), dtype=np.uint8)
    return cv2.imdecode(buffer, cv2.IMREAD_COLOR)


def infer():
    frame = decode_upload()
    if frame is None:
        return None, (jsonify(error="Provide a valid image in the 'image' form field."), 400)
    try:
        return (frame, get_detector().detect(frame)), None
    except ModelUnavailableError as error:
        return None, (jsonify(error=str(error)), 503)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/predict")
def predict():
    result, error = infer()
    if error:
        return error
    _, predictions = result
    return jsonify(faces=[prediction.to_dict() for prediction in predictions])


@app.post("/api/annotate")
def annotate():
    result, error = infer()
    if error:
        return error
    frame, predictions = result
    ok, encoded = cv2.imencode(".jpg", get_detector().annotate(frame, predictions))
    if not ok:
        return jsonify(error="Could not encode image."), 500
    from io import BytesIO
    return send_file(BytesIO(encoded.tobytes()), mimetype="image/jpeg", download_name="annotated.jpg")


@app.errorhandler(413)
def oversized_file(_error):
    return jsonify(error="Image must be 8 MB or smaller."), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
