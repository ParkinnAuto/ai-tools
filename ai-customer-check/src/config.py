# Camera
CAMERA_INDEX = 0

# Window
WINDOW_NAME = "AI Customer Check"

# Keyboard
QUIT_KEYS = ["q", "Q"]

# YOLO Model
MODEL_PATH = "yolov8n-pose.pt"

# Detection Settings
WAITING_THRESHOLD = 10 # seconds before first alert
ALERT_COOLDOWN = 30 # seconds before repeating alert
EXIT_RESET_TIME = 10 # seconds before resetting when zone is empty

# Customer waiting zone
# Format: x1, y1, x2, y2
CUSTOMER_ZONE = (100,100,500,400)

# Alert sound
ALERT_SOUND_PATH = "assets/alert.wav"

 # Log path
LOG_PATH = "logs/detections.csv"

# Delete logs older than this number of days
LOG_RETENTION_DAYS = 3