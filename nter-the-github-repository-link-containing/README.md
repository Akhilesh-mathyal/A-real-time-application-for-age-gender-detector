# Real-Time Gender and Age Detector

A privacy-aware web application that estimates **apparent age range** and **perceived gender presentation** from a webcam or uploaded image. It uses OpenCV's DNN face detector and the public Levi & Hassner Caffe age/gender models.

> **Important:** These predictions are probabilistic visual estimates, not a determination of a person's actual age, identity, or gender. Do not use this application for hiring, admissions, policing, access control, or any high-impact decision.

## Features

- Live webcam inference in the browser
- Image upload and annotated result download
- Face detection, age-range prediction, and gender-presentation prediction
- Confidence scores and clear "no face found" results
- Flask JSON API for integration
- Unit tests that run without downloading ML model files

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/download_models.py
python app.py
```

Open `http://127.0.0.1:5000` and allow camera access. Press `q` only if using the optional desktop script.

## Test

```powershell
pytest -q
```

## Project structure

```
app.py                 Flask application and JSON endpoints
detector.py            DNN loading, preprocessing, inference, annotations
templates/index.html   Browser UI
static/                CSS and browser JavaScript
scripts/               Model downloader and optional desktop camera runner
tests/                 Unit/API tests
docs/                  Setup, API, ethics, and dataset documentation
models/                Downloaded model files (not committed)
```

## API

`POST /api/predict` accepts a multipart form field named `image` and returns:

```json
{"faces": [{"box": [x1, y1, x2, y2], "age": "25-32", "age_confidence": 0.91,
"gender_presentation": "Female", "gender_confidence": 0.88}]}
```

Use `POST /api/annotate` with the same field to receive an annotated JPEG.

See [docs/SETUP.md](docs/SETUP.md), [docs/DATASETS.md](docs/DATASETS.md), and [docs/ETHICS.md](docs/ETHICS.md) for the full documentation.

## Submission links

Replace these placeholders after publishing your own copies:

- GitHub repository: `https://github.com/<your-account>/gender-age-detector`
- Google Drive dataset folder: `https://drive.google.com/drive/folders/<your-folder-id>`

The dataset folder should contain only material you are licensed to share. The downloadable inference weights are deliberately excluded from this repository; run `scripts/download_models.py` instead.
