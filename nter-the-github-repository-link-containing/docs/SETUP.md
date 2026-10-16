# Setup guide

## Requirements

- Python 3.10 or newer
- A webcam (only for live mode)
- Internet access once, to download public model artifacts

## Install

From the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/download_models.py
python app.py
```

Browse to `http://127.0.0.1:5000`. The browser UI can use the camera or upload a JPEG/PNG. Camera access normally requires `localhost` or HTTPS.

## Troubleshooting

- **"Model files are missing"** — Run `python scripts/download_models.py` from the repository root.
- **Camera denied** — allow camera access in the browser; image upload remains available.
- **Poor result** — use a well-lit, front-facing image. The models are less reliable with occlusion, extreme pose, or low resolution.
- **Port busy** — set another port: `$env:PORT=5050; python app.py`.
