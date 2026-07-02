import csv
import os
from datetime import datetime, timedelta

def write_log(message, log_path = "logs/detections.csv"):
    # Create logs folder if it does not exist
    os.makedirs(os.path .dirname(log_path), exist_ok=True)

    # Check if log file already exists
    file_exists = os.path.exists(log_path)

    with open(log_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header only when file is new
        if not file_exists:
            writer.writerow(["timestamp", "event"])

        # Write event row
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message,
        ])
    
def cleanup_old_logs(log_path="logs/detections.csv", retention_days=3):
    # If log file does not exist, do nothing
    if not os.path.exists(log_path):
        return

    cutoff_date = datetime.now() - timedelta(days=retention_days)

    kept_rows = []

    with open(log_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                log_time = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")

                # Keep only logs newer than cutoff date
                if log_time >= cutoff_date:
                    kept_rows.append(row)

            except Exception:
                # Skip broken or invalid log rows
                continue

    with open(log_path, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["timestamp", "event"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(kept_rows)