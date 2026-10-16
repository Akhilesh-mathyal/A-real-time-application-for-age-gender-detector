"""Optional desktop OpenCV viewer for webcam inference."""
import cv2
from detector import AgeGenderDetector

detector = AgeGenderDetector()
camera = cv2.VideoCapture(0)
if not camera.isOpened(): raise SystemExit("Could not open a camera.")
while True:
    ok, frame = camera.read()
    if not ok: break
    cv2.imshow("Age & Gender Detector", detector.annotate(frame, detector.detect(frame)))
    if cv2.waitKey(1) & 0xFF == ord("q"): break
camera.release(); cv2.destroyAllWindows()
