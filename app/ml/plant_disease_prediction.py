import numpy as np
import tensorflow as tf
import cv2

model = tf.keras.models.load_model("trained_model.keras")

class_names = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy",
]


# Original code, for standalone use / testing etc.
def batched_prediction():
    image_path = "leaf.JPG"

    image_paths = [
        "real_leaves/IMG_4129.JPG",
        "real_leaves/IMG_4130.JPG",
        "real_leaves/IMG_4131.JPG",
        "real_leaves/IMG_4132.JPG",
        "real_leaves/IMG_4133.JPG",
        "real_leaves/IMG_4134.JPG",
    ]

    for sample in image_paths:
        print(sample)
        img = cv2.imread(sample)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        image = tf.keras.preprocessing.image.load_img(
            image_path, target_size=(256, 256)
        )
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])  # Convert single image to a batch
        # unsure if needed, since we're processing each image in a loop currently.
        # might come in handy later.

        prediction = model.predict(input_arr)

        result_index = np.argmax(prediction)

        print(f"This picture shows that the leaf is {class_names[result_index]}")


# This is used for the flask side.
def single_prediction(filepath):
    # TODO - at some point I need to figure out where to include class names,
    # probably not hardcoded inside the function, maybe call from here to go fetch them
    # depending on what kind of plant the user has specified, this works for now, but isn't optimal.
    class_names = [
        "Pepper__bell___Bacterial_spot",
        "Pepper__bell___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
        "Tomato_Bacterial_spot",
        "Tomato_Early_blight",
        "Tomato_Late_blight",
        "Tomato_Leaf_Mold",
        "Tomato_Septoria_leaf_spot",
        "Tomato_Spider_mites_Two_spotted_spider_mite",
        "Tomato__Target_Spot",
        "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "Tomato__Tomato_mosaic_virus",
        "Tomato_healthy",
    ]

    img = cv2.imread(filepath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    image = tf.keras.preprocessing.image.load_img(filepath, target_size=(256, 256))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to a batch
    # unsure if needed, since we're processing each image in a loop currently.
    # might come in handy later.

    prediction = model.predict(input_arr)

    result_index = np.argmax(prediction)

    return f"This picture shows that the leaf is {class_names[result_index]}"
