"""Download public model artifacts required for inference."""
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "models"
BASE = "https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender"
FILES = ["opencv_face_detector.pbtxt", "opencv_face_detector_uint8.pb", "age_deploy.prototxt", "age_net.caffemodel", "gender_deploy.prototxt", "gender_net.caffemodel"]

def main():
    TARGET.mkdir(exist_ok=True)
    for name in FILES:
        destination = TARGET / name
        if destination.exists():
            print(f"Exists: {name}")
            continue
        print(f"Downloading: {name}")
        urlretrieve(f"{BASE}/{name}", destination)
    print("Models are ready.")

if __name__ == "__main__": main()
