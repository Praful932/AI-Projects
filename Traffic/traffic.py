import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
NUM_CATEGORIES_SMALL = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    print(len(images), len(labels))
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()
    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    for i in range(NUM_CATEGORIES):
        data_folder = os.path.join(data_dir, str(i))
        # Read images from each class
        for image in os.listdir(data_folder):
            image_path = os.path.join(data_folder, image)
            img = cv2.imread(image_path)
            images.append(cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))/255.0)
            labels.append(i)

    dataset = (images, labels)
    return dataset


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.Sequential([
        # 2 Convolutional Layers
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                               input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add Dense layer
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),

        # Add output layer
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    print(model.summary())

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def visualize():
    data_folder = 'gtsrb'
    fig, ax = plt.subplots(figsize=(20, 20), nrows=5, ncols=8)
    category = 0
    for i in range(5):
        for j in range(8):
            image_path = os.path.join(os.path.join('gtsrb', str(category)))
            image_no = np.random.randint(len(os.listdir(image_path)))
            image_path = os.path.join(
                image_path, os.listdir(image_path)[image_no])
            img = cv2.imread(image_path)
            # image = cv2.resize(img,(IMG_WIDTH, IMG_HEIGHT))
            ax[i, j].axis("off")
            ax[i, j].imshow(img)
            ax[i, j].set_title(label_map[str(category)])
            category += 1


if __name__ == "__main__":
    main()
