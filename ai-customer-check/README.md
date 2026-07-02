# AI Customer Check

A computer vision prototype for small family shops.  
The system detects whether a person is waiting inside a predefined customer zone and triggers an audio alert when the waiting time exceeds a configurable threshold.

## Features

- Real-time camera detection
- Person detection using YOLO Pose
- Custom customer waiting zone
- Waiting-time based alert logic
- Audio alert with cooldown
- CSV event logging
- Automatic log cleanup

## Tech Stack

- Python
- OpenCV
- Ultralytics YOLO
- Pygame
- CSV logging

## Project Structure

```text
ai-customer-check/
├── main.py
├── src/
│   ├── config.py
│   ├── detector.py
│   ├── zone.py
│   ├── alert.py
│   └── logger.py
├── assets/
│   └── alert.wav
├── logs/
│   └── detections.csv
├── requirements.txt
└── README.md

## How It Works
Camera
→ YOLO detects person
→ Check if person is inside customer zone
→ Start waiting timer
→ Trigger alert after threshold
→ Repeat alert after cooldown
→ Save event to CSV log

## How to run
pip install -r requirements.txt
python main.py

## Configuration
Edit src/config.py to adjust camera, zone, alert time, cooldown, sound path, and log retention.

## Test Results

The current version has been tested locally using a laptop webcam.

The test confirmed that the system can:

- Detect a person inside the predefined customer zone
- Start counting waiting time
- Trigger an audio alert after the waiting threshold
- Repeat the alert after the cooldown period
- Save alert events into a CSV log file

A real shop environment test has not been performed yet.

For detailed local test results, see [`tests/README.md`](tests/README.md).

## Future Improvements

- Test the system in a real shop environment
- Adjust the Customer Zone based on the actual camera angle
- Deploy the system on Raspberry Pi or a mini PC
- Add support for IP cameras or CCTV camera streams
- Improve customer detection accuracy in different lighting conditions
- Add a simple configuration file for easier zone and timer adjustment
- Add optional remote notification support, such as sending alerts to a phone