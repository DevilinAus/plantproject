import os

import tensorflow as tf
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Input, Dropout
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Enable float16 mixed precision for Tensor Core acceleration.
# This speeds up training significantly on NVIDIA GPUs with Tensor Cores,
# including RTX 20xx, 30xx, and 40xx series (Turing, Ampere, Ada Lovelace architectures).
# On CPUs or older GPUs, this may have no benefit or cause instability.
if tf.config.list_physical_devices("GPU"):
    from keras.mixed_precision import set_global_policy

    set_global_policy("mixed_float16")

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

    # Enable prefetching, this allows CPU to prep the next dataset whilst the GPU is working. Zoomies!
    # Speed increase from this is most noticable between each run, there's no longer delay.
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

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

    # 512
    model.add(
        Conv2D(
            filters=512,
            kernel_size=3,
            padding="same",
            activation="relu",
        )
    )

    model.add(Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=2, strides=2))

    # ===============================================
    #    FINE TUNING RESULTS
    #
    #  pre = 0.25 post = none. 94.4% best.
    #  pre = 0.25 post = 0.10  95.3% best.
    #  pre = 0.25 post = 0.20  96.0% best.
    #  pre = 0.25 post = 0.30  94.9% best.
    #  pre = 0.25 post = 0.40  92.2% best.
    #  Further tuning to pre numbers might help dial this slightly higher.

    pre_dropout = 0.25
    post_dropout = 0.1

    # Add dropout. This disables a percentage of neurons during training to avoid overfitting (think memorisation.)
    model.add(Dropout(pre_dropout))

    model.add(Flatten())
    model.add(Dense(units=1500, activation="relu"))

    # Add post flattern dropout. (best prior 94.4%)
    model.add(Dropout(post_dropout))

    # Callback for early stopping, should automatically help with dialing in learning and avoid overstepping
    early_stop = EarlyStopping(
        monitor="val_loss", patience=5, restore_best_weights=True
    )

    # Output Layer
    model.add(Dense(units=total_units, activation="softmax"))

    # Adjust learning rate here to prevent overshoot.
    adam_override = Adam(learning_rate=0.00001)

    # Compile Model
    model.compile(
        optimizer=adam_override, loss="categorical_crossentropy", metrics=["accuracy"]
    )

    model.summary()

    # Model Training

    training_history = model.fit(
        x=train_ds, validation_data=val_ds, epochs=50, callbacks=[early_stop]
    )


main()
