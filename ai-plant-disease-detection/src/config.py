# Dataset
DATASET_NAME = "BrandonFors/Plant-Diseases-PlantVillage-Dataset"

# Project setting
PROJECT_NAME = "potato"

# Image setting
IMAGE_SIZE = 256
BATCH = 32
SHUFFLE_BUFFER_SIZE = 42

# Training setting
EPOCHS = 10
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42

# Classes we want to use first
SELECTED_CLASSES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
]

# Output paths
MODEL_PATH = "models/potato_cnn.keras"
CLASS_NAMES_PATH = "models/potato_class_names.json"

ACCURACY_LOSS_PLOT_GRAPH = "outputs/plots/potato_accuracy_loss.png"
CONFUSION_MATRIX_PATH = "outputs/plots/potato_confusion_matrix.png"
REPORT_PATH = "outputs/reports/potato_report.txt"