import cv2
import time
import os
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
motion_detected = False

def start_detection(save_interval=0.5):
    global motion_detected
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    save_dir = "captured_images"
    os.makedirs(save_dir, exist_ok=True)
    last_saved = time.time()

    while True:
        if not motion_detected:
            time.sleep(0.1)
            continue

        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()

        # Save image every 0.5 seconds
        if time.time() - last_saved >= save_interval:
            filename = os.path.join(save_dir, f"person_{int(time.time())}.jpg")
            cv2.imwrite(filename, frame)
            last_saved = time.time()

        cv2.imshow('YOLOv8 Webcam Detection', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()