import cv2
from ultralytics import YOLO

# Settings
MODEL_NAME = "yolov8n.pt"
CAMERA_INDEX = 0

CONFIDENCE_THRESHOLD = 0.5

# Main
def main():
    print("Loading YOLO model...")
    model = YOLO(MODEL_NAME)
    print("YOLO model loaded")

    # Open camera
    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not camera.isOpened():
        print("Cannot open camera")
        return
    
    window_name = "AI YOLO Object Detection"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("Camera started")
    print("Press Q or ESC to quit")
    print("Press S to save scrennshot")

    while True:
        success, frame = camera.read()

        if not success:
            print("Cannot read camera frame")
            break

        # Run YOLO Detection
        results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

        # Draw detection results on frame
        annotated_frame = results[0].plot()

        cv2.putText(
            annotated_frame,
            "YOLO Object Detection | Q: Quit | S: Save Screenshot",
            (20,40),
            cv2.FONT_HERSHEY_COMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.imshow(window_name,annotated_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            print("Closing camera...")
            break

        elif key == ord("s") or key == ord("S"):
            save_path = "captures/detection_screenshot.jpg"
            cv2.imwrite(save_path,annotated_frame)
            print(f"Screenshot saved to {save_path}")
        
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()