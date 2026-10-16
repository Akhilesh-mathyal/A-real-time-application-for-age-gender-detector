import numpy as np
import pytest

from detector import AgeGenderDetector, ModelUnavailableError, Prediction


def test_missing_models_produces_actionable_error(tmp_path):
    with pytest.raises(ModelUnavailableError, match="download_models"):
        AgeGenderDetector(tmp_path)


def test_prediction_serializes_cleanly():
    prediction = Prediction((1, 2, 3, 4), "25-32", 0.91234, "Female", 0.81234)
    assert prediction.to_dict() == {"box": [1, 2, 3, 4], "age": "25-32", "age_confidence": 0.9123, "gender_presentation": "Female", "gender_confidence": 0.8123}


def test_annotation_returns_image():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    rendered = AgeGenderDetector.annotate(image, [Prediction((10, 20, 70, 80), "25-32", .9, "Male", .8)])
    assert rendered.shape == image.shape
    assert np.any(rendered != image)
