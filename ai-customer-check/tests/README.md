# Test Results

## AI Customer Check - Local Camera Test

This document summarizes the test result of the **AI Customer Check** prototype.

The purpose of this test was to verify that the system can detect a person inside a predefined customer waiting zone, count the waiting time, trigger an audio alert, repeat the alert after a cooldown period, and save alert events into a CSV log file.

---

## Test Environment

- Camera: Laptop webcam
- Model: YOLO Pose
- Computer Vision Library: OpenCV
- Alert Type: Audio alert
- Log Format: CSV
- Test Mode: Local real-time camera test

---

## Test Objectives

The test was designed to confirm the following features:

- Detect whether a person is inside the predefined Customer Zone
- Display the correct zone status on the camera window
- Start counting waiting time when a person enters the zone
- Trigger an alert after the waiting time exceeds the configured threshold
- Prevent repeated alerts from playing continuously
- Repeat the alert after the cooldown period if the person is still inside the zone
- Save alert events into a CSV log file

---

## Test Scenario 1: No Person in Customer Zone

At the beginning of the test, no person was inside the predefined Customer Zone.

The system correctly displayed:

```text
No person in zone

This confirms that the system can recognize when the Customer Zone is empty and does not trigger an unnecessary alert.

---

## Test Scenario 2: Person Detected Inside Customer Zone

A person then entered the predefined Customer Zone.

The system successfully detected the person and displayed:

Person in zone
Waiting time: 5.9s

This confirms that the system can detect a person inside the Customer Zone and start counting how long the person has stayed in the zone.

---

# Test Scenario 3: Alert Triggered and Cooldown Started

After the person stayed inside the Customer Zone long enough, the system triggered an alert and entered cooldown mode.

The system displayed:

Person in zone
Waiting time: 13.1s
Cooldown: 27.0s

This confirms that the alert was triggered successfully and that the cooldown system started working after the alert.

---

# CSV Log Output

The system successfully saved the alert events into a CSV log file.

Example log output:

timestamp,event
2026-07-03 00:43:06,Alert triggered
2026-07-03 00:43:37,Alert triggered again

The log confirms that:

The first alert was triggered at 2026-07-03 00:43:06
The repeated alert was triggered at 2026-07-03 00:43:37
The cooldown-based repeated alert system worked correctly
Alert events were successfully saved into the log file
Test Result

The test was successful.

The system correctly performed the expected workflow:

No person in zone
→ Person enters Customer Zone
→ Waiting timer starts
→ Alert is triggered after the threshold
→ Cooldown starts
→ Alert is repeated after cooldown
→ Events are saved to CSV log

---

## Screenshots

### No Person in Zone

![No Person in Zone](screenshots/no_person_in_zone.png)

### Person in Zone

![Person in Zone](screenshots/person_in_zone.png)

### Cooldown Alert

![Cooldown Alert](screenshots/cooldown_alert.png)
---

# Conclusion

The current prototype successfully detects a person waiting inside a predefined customer area and sends an audio alert when the waiting time exceeds the configured threshold.

The system also prevents continuous repeated alerts by using a cooldown mechanism and records alert events into a CSV log file.

This confirms that the main prototype logic is working as expected and is ready to be documented as a working computer vision prototype for a small shop customer alert system.