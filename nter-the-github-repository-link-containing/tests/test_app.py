import io
import numpy as np
import cv2

import app as application
from detector import Prediction


class FakeDetector:
    def detect(self, _frame):
        return [Prediction((1, 2, 30, 40), "25-32", .9, "Female", .8)]

    @staticmethod
    def annotate(frame, predictions):
        from detector import AgeGenderDetector
        return AgeGenderDetector.annotate(frame, predictions)


def image_bytes():
    ok, encoded = cv2.imencode(".jpg", np.zeros((50, 50, 3), dtype=np.uint8))
    assert ok
    return io.BytesIO(encoded.tobytes())


def test_predict_requires_image():
    client = application.app.test_client()
    response = client.post("/api/predict")
    assert response.status_code == 400


def test_predict_returns_predictions(monkeypatch):
    application.get_detector.cache_clear()
    monkeypatch.setattr(application, "get_detector", lambda: FakeDetector())
    client = application.app.test_client()
    response = client.post("/api/predict", data={"image": (image_bytes(), "test.jpg")})
    assert response.status_code == 200
    assert response.json["faces"][0]["age"] == "25-32"
