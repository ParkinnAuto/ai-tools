# MNIST Image Classification with TensorFlow/Keras

This project is a simple deep learning image classification project using **TensorFlow** and **Keras**.
The model is trained on the **MNIST dataset**, which contains handwritten digit images from `0` to `9`.

The goal of this project is to understand the basic workflow of deep learning image classification:

```txt
Load dataset
→ Preprocess images
→ Build neural network model
→ Train model
→ Evaluate model
→ Save model
→ Load model for prediction
```

---

## Project Overview

This project trains a neural network to classify handwritten digits.

Example:

```txt
Input image: handwritten digit
Output: predicted number from 0 to 9
```

The trained model achieved approximately:

```txt
Test accuracy: 97.8%
Test loss: 0.082
```

---

## Tech Stack

* Python
* TensorFlow
* Keras
* NumPy
* Matplotlib
* MNIST dataset

---

## Project Structure

```txt
dl-object-detection/
├── venv/
├── src/
│   ├── train_mnist.py
│   └── predict_mnist.py
├── models/
│   └── mnist_model.h5
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Dataset

This project uses the built-in MNIST dataset from TensorFlow/Keras.

MNIST contains:

```txt
60,000 training images
10,000 test images
Image size: 28x28 pixels
Classes: 0-9
```

Each image is a grayscale handwritten digit.

---

## How It Works

### 1. Load Dataset

```python
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
```

The dataset is split into:

```txt
x_train = training images
y_train = training labels

x_test = test images
y_test = test labels
```

---

### 2. Normalize Images

Pixel values originally range from `0` to `255`.

They are normalized to the range `0` to `1`:

```python
x_train = x_train / 255.0
x_test = x_test / 255.0
```

Only image data should be normalized.

Labels such as `0`, `1`, `2`, ..., `9` should not be normalized.

---

### 3. Build the Model

The model uses a simple neural network:

```python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])
```

Explanation:

```txt
Flatten layer:
Converts a 28x28 image into a 1D vector.

Dense 128:
Learns patterns from the image.

Dense 10:
Outputs probabilities for digits 0-9.
```

---

### 4. Train the Model

```python
model.fit(
    x_train,
    y_train,
    epochs=10,
    validation_data=(x_test, y_test)
)
```

The model learns from the training images and labels.

---

### 5. Evaluate the Model

```python
test_loss, test_accuracy = model.evaluate(x_test, y_test)
```

Example result:

```txt
Test loss: 0.082
Test accuracy: 0.978
```

This means the model correctly classified around 97.8% of the test images.

---

### 6. Save the Model

```python
model.save("models/mnist_model.h5")
```

The trained model is saved so it can be used later without training again.

---

### 7. Predict with Saved Model

The prediction script loads the saved model:

```python
model = tf.keras.models.load_model("models/mnist_model.h5")
```

Then it predicts a digit from a test image.

---

## Installation

### 1. Create Virtual Environment

```powershell
python -m venv venv
```

### 2. Activate Virtual Environment

For PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

If installing manually:

```powershell
pip install numpy==1.23.5 tensorflow==2.10.1 matplotlib opencv-python scikit-learn pillow
```

---

## Usage

### Train the Model

```powershell
python src/train_mnist.py
```

This will:

```txt
Load MNIST dataset
Normalize image data
Build the neural network
Train the model
Evaluate accuracy
Save the trained model
```

The trained model will be saved to:

```txt
models/mnist_model.h5
```

---

### Predict a Digit

```powershell
python src/predict_mnist.py
```

This will:

```txt
Load the saved model
Pick a test image
Predict the digit
Show the image with predicted result
```

---

## Result

Example result after training:

```txt
Test loss: 0.08247870206832886
Test accuracy: 0.9781000018119812
```

This means the model reached around:

```txt
97.81% accuracy
```

---

## Important Notes

This project is image classification, not object detection.

```txt
Image Classification:
Predicts what the image is.

Object Detection:
Predicts what objects are in the image and where they are located.
```

MNIST is a beginner-friendly dataset for learning the basic workflow of deep learning.

---

## What I Learned

Through this project, I learned:

* How to create a Python virtual environment
* How to install TensorFlow and Keras
* How to load and preprocess image datasets
* How to build a neural network using `tf.keras`
* How to train and evaluate a model
* How to save and load a trained model
* How to use the trained model for prediction

---

## Future Improvements

Possible improvements for this project:

* Try a Convolutional Neural Network model
* Test with custom handwritten digit images
* Add a confusion matrix
* Add prediction confidence score
* Build a simple web interface for uploading images
* Convert the model to TensorFlow Lite

---

## Author

Parkin Arsanamanee