import tensorflow as tf
import matplotlib.pyplot as plt

# 1. Load MNIST dataset
mnist = tf.keras.datasets.mnist

(x_train,y_train), (x_test,y_test) = mnist.load_data()

print("Training images shape: ", x_train.shape)
print("Training labels shape: ", y_train.shape)
print("Test images shape: ", x_test.shape)
print("Test lables shape: ", y_test.shape)


# 2. Normalize images
# Normal pixel has value from 0-255
# We will change it to become 0-1 so the model can understand it easier

x_train = x_train/255.0
x_test = x_test/255.0


# 3. Show one sample image

# Colored image
#plt.imshow(x_train[0])

# Black-White image
plt.imshow(x_train[0],cmap="grey")
plt.title(f"label: {y_train[0]}")
plt.show()


# 4. Building model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28)),

    tf.keras.layers.Dense(128, activation="relu"),

    tf.keras.layers.Dense(10, activation="softmax")
])


# 5. Compile model
model.compile(
    optimizer = "adam",
    loss = "sparse_categorical_crossentropy",
    metrics = ["accuracy"]
)

# 6. Train model
model.fit(
    x_train,
    y_train,
    epochs = 10,
    #validation_data = (x_test,y_test)
)

# 7. Evaluate model
test_loss, test_accuracy = model.evaluate(x_test,y_test)

print("Test loss: ", test_loss)
print("Test accuracy: ", test_accuracy)

# 8. Save model
model.save("model/mnist_model.h5")
print("Model saved to models/mnist_model.h5")