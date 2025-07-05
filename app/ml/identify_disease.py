from flask import Blueprint, render_template, request, url_for, redirect
from app.ml.plant_disease_prediction import single_prediction
import os


from app.db.flask_db import db


identify_disease_bp = Blueprint(
    "disease_predict_bp",
    __name__,
    template_folder="templates",
)


@identify_disease_bp.route("/identify_disease_page", methods=["GET", "POST"])
def identify_disease():
    if request.method == "POST":
        image = request.files.get("image")
        # plant_type = request.form.get("plant_type") Not yet implemented

        if image and image.filename:
            file_path = os.path.join("uploads", image.filename)
            os.makedirs(
                "uploads", exist_ok=True
            )  # This seems inefficient to put it here, maybe should be created on app launch?
            image.save(file_path)

            # TODO implement passing the image across here.
            prediction = single_prediction(file_path)

            return redirect(
                url_for("disease_predict_bp.show_results", prediction=prediction)
            )

    return render_template(
        "identify_disease_page.html",
    )


@identify_disease_bp.route("/show_results", methods=["GET", "POST"])
def show_results():
    prediction = request.args.get("prediction", "No prediction received")
    return f"Prediction result: {prediction}"
