import cv2
import time

from src.config import (
    CAMERA_INDEX,
    WINDOW_NAME,
    MODEL_PATH,
    CUSTOMER_ZONE,
    WAITING_THRESHOLD,
    ALERT_COOLDOWN,
    ALERT_SOUND_PATH,
    QUIT_KEYS,
    LOG_PATH,
    LOG_RETENTION_DAYS
)
from src.detector import CustomerDetector
from src.zone import draw_zone, get_box_center, is_point_inside_zone
from src.alert import AlertPlayer
from src.logger import write_log, cleanup_old_logs

detector = CustomerDetector(MODEL_PATH)
alert_player = AlertPlayer(ALERT_SOUND_PATH)

cap = cv2.VideoCapture(CAMERA_INDEX)
cleanup_old_logs(LOG_PATH, LOG_RETENTION_DAYS)

zone_start_time = None
last_alert_time = None

while True:
    ret, frame = cap.read()

    if not ret:
        print("Cannot read from camera")
        break

    result = detector.detect(frame)

    # Draw result from YOLO to the picture
    annotated_frame = result.plot()

    annotated_frame = draw_zone(annotated_frame, CUSTOMER_ZONE)

    person_in_zone = False

    # Check whether has box from YOLO
    if result.boxes is not None:
        for box in result.boxes:
            # get human's marking from YOLO
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # find middle point of person
            center = get_box_center((x1, y1, x2, y2))

            # draw middle point on person
            cv2.circle(annotated_frame, center, 5, (0, 0, 255), -1)

            # Check whether middle point is in Customer Zone
            if is_point_inside_zone(center, CUSTOMER_ZONE):
                person_in_zone = True

    if person_in_zone:
        # If this is the first time seeing person in zone, start timer
        if zone_start_time is None:
            zone_start_time = time.time()

        # Calculate how long person has stayed in zone
        waiting_time = time.time() - zone_start_time

        cv2.putText(
            annotated_frame,
            "Person in zone",
            (30, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Waiting time: {waiting_time:.1f}s",
            (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )

        if waiting_time >= WAITING_THRESHOLD:
            current_time = time.time()

            # First Alert
            if last_alert_time is None:
                last_alert_time = current_time

                # Play alert sound
                alert_player.play()

                # Write alert log
                write_log("Alert triggered", LOG_PATH)

                cv2.putText(
                    annotated_frame,
                    "Alert triggered",
                    (30, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

            # Repeat alert after cooldown
            elif current_time - last_alert_time >= ALERT_COOLDOWN:
                last_alert_time = current_time

                # Play alert sound
                alert_player.play()

                # Write alert log
                write_log("Alert triggered again", LOG_PATH)

                cv2.putText(
                    annotated_frame,
                    "Alert triggered again",
                    (30, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

            # During cooldown
            else:
                cooldown_left = ALERT_COOLDOWN - (current_time - last_alert_time)

                cv2.putText(
                    annotated_frame,
                    f"Cooldown: {cooldown_left:.1f}s",
                    (30, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                )

    else:
        # If no person in zone, reset timer
        zone_start_time = None
        last_alert_time = None

        cv2.putText(
            annotated_frame,
            "No person in zone",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    # Resize video display
    annotated_frame = cv2.resize(annotated_frame, (1280, 720))

    cv2.imshow(WINDOW_NAME, annotated_frame)

    key = cv2.waitKey(1) & 0xFF

    if chr(key) in QUIT_KEYS:
        break

cap.release()
cv2.destroyAllWindows()