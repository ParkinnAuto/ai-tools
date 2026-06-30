import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

# 1. Load test data
mnist = tf.keras.datasets.mnist
(_,_), (x_test,y_test) = mnist.load_data()
x_test = x_test/255.0


# 2. Load trained model
model = tf.keras.models.load_model("model/mnist_model.h5")


# 3. Pick one image
index = 0
image = x_test[index]
true_label = y_test[index]


# 4. Predict
prediction = model.predict(np.array([image]))
predicted_label = np.argmax(prediction)


# 5. Show result
print("True label:", true_label)
print("Predicted label:", predicted_label)

plt.imshow(image, cmap="grey")
plt.title(f"Predicted: {predicted_label} | True: {true_label}")
plt.show()