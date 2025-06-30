import os
import tensorflow as tf
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
    train_ds, val_ds = data_preprocess(training_directory)


main()
