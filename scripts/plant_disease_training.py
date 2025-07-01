import os
import tensorflow as tf
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Input
from keras.models import Sequential
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
training_directory = os.path.join(project_root, "training_data", "PlantVillage")


print(f"Training directory is: {training_directory}")


def data_preprocess(training_directory):
    # Since we don't have a split set of training data, need to manually assign 20% for validation
    train_ds = tf.keras.utils.image_dataset_from_directory(
        training_directory,
        labels="inferred",
        label_mode="categorical",
        class_names=None,
        color_mode="rgb",
        batch_size=32,
        image_size=(256, 256),
        shuffle=True,
        seed=123,
        validation_split=0.2,
        subset="training",
        interpolation="bilinear",
        follow_links=False,
        crop_to_aspect_ratio=False,
        pad_to_aspect_ratio=False,
        data_format=None,
        verbose=True,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        training_directory,
        labels="inferred",
        label_mode="categorical",
        class_names=None,
        color_mode="rgb",
        batch_size=32,
        image_size=(256, 256),
        shuffle=True,
        seed=123,
        validation_split=0.2,
        subset="validation",
        interpolation="bilinear",
        follow_links=False,
        crop_to_aspect_ratio=False,
        pad_to_aspect_ratio=False,
        data_format=None,
        verbose=True,
    )

    return train_ds, val_ds


def main():
    # This should be adjusted for the total amount of classes(each folder of one classification,
    # is one class, this will be outputted "Found 20638 files belonging to 15 classes")
    total_units = 15

    train_ds, val_ds = data_preprocess(training_directory)

    model = Sequential()
    model.add(Input(shape=(256, 256, 3)))

    # TODO: build helper function to cut down the amount of copy pasted code in this next section.
    # 32
    model.add(
        Conv2D(
            filters=32,
            kernel_size=3,
            padding="same",
            activation="relu",
        )
    )

    model.add(Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=2, strides=2))

    # 64
    model.add(
        Conv2D(
            filters=64,
            kernel_size=3,
            padding="same",
            activation="relu",
        )
    )

    model.add(Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=2, strides=2))

    # 128
    model.add(
        Conv2D(
            filters=128,
            kernel_size=3,
            padding="same",
            activation="relu",
        )
    )

    model.add(Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=2, strides=2))

    # 256
    model.add(
        Conv2D(
            filters=256,
            kernel_size=3,
            padding="same",
            activation="relu",
        )
    )

    model.add(Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=2, strides=2))

    model.add(Flatten())
    model.add(Dense(units=1024, activation="relu"))

    # Output Layer
    model.add(Dense(units=total_units, activation="softmax"))

    # Compile Model
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    model.summary()

main()
