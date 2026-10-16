"""OpenCV DNN-based face, apparent-age, and gender-presentation estimation."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np

MODEL_DIR = Path(__file__).parent / "models"
AGE_BUCKETS = ["0-2", "4-6", "8-12", "15-20", "25-32", "38-43", "48-53", "60-100"]
GENDER_LABELS = ["Male", "Female"]
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)


@dataclass
class Prediction:
    box: tuple[int, int, int, int]
    age: str
    age_confidence: float
    gender_presentation: str
    gender_confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "box": list(self.box),
            "age": self.age,
            "age_confidence": round(self.age_confidence, 4),
            "gender_presentation": self.gender_presentation,
            "gender_confidence": round(self.gender_confidence, 4),
        }


class ModelUnavailableError(RuntimeError):
    """Raised when the required downloaded model artifacts are absent."""


class AgeGenderDetector:
    def __init__(self, model_dir: Path = MODEL_DIR, confidence_threshold: float = 0.7):
        self.model_dir = Path(model_dir)
        self.confidence_threshold = confidence_threshold
        self.face_net = self._load_net("opencv_face_detector_uint8.pb", "opencv_face_detector.pbtxt")
        self.age_net = self._load_net("age_net.caffemodel", "age_deploy.prototxt")
        self.gender_net = self._load_net("gender_net.caffemodel", "gender_deploy.prototxt")

    def _load_net(self, weights: str, config: str):
        weight_path, config_path = self.model_dir / weights, self.model_dir / config
        if not weight_path.exists() or not config_path.exists():
            raise ModelUnavailableError(
                "Model files are missing. Run: python scripts/download_models.py"
            )
        return cv2.dnn.readNet(str(weight_path), str(config_path))

    def detect(self, frame: np.ndarray) -> list[Prediction]:
        if frame is None or frame.size == 0:
            return []
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], swapRB=False)
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        predictions: list[Prediction] = []
        for index in range(detections.shape[2]):
            confidence = float(detections[0, 0, index, 2])
            if confidence < self.confidence_threshold:
                continue
            x1, y1, x2, y2 = (detections[0, 0, index, 3:7] * [width, height, width, height]).astype(int)
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(width, x2), min(height, y2)
            face = frame[y1:y2, x1:x2]
            if face.size == 0:
                continue
            predictions.append(self._classify(face, (x1, y1, x2, y2)))
        return predictions

    def _classify(self, face: np.ndarray, box: tuple[int, int, int, int]) -> Prediction:
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        self.gender_net.setInput(blob)
        gender_scores = self.gender_net.forward()[0]
        self.age_net.setInput(blob)
        age_scores = self.age_net.forward()[0]
        gender_index, age_index = int(np.argmax(gender_scores)), int(np.argmax(age_scores))
        return Prediction(
            box=box,
            age=AGE_BUCKETS[age_index], age_confidence=float(age_scores[age_index]),
            gender_presentation=GENDER_LABELS[gender_index], gender_confidence=float(gender_scores[gender_index]),
        )

    @staticmethod
    def annotate(frame: np.ndarray, predictions: list[Prediction]) -> np.ndarray:
        result = frame.copy()
        for prediction in predictions:
            x1, y1, x2, y2 = prediction.box
            label = f"{prediction.gender_presentation} | {prediction.age}"
            cv2.rectangle(result, (x1, y1), (x2, y2), (0, 220, 100), 2)
            cv2.putText(result, label, (x1, max(22, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 100), 2)
        return result
