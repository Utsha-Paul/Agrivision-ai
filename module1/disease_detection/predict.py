import os
import json
import numpy as np

try:
    from keras.models import load_model
    from keras.utils import load_img, img_to_array
except ImportError:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.utils import load_img, img_to_array


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "disease",
    "disease_efficientnet.keras"
)

CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "disease",
    "class_names.json"
)

IMAGE_SIZE = (224, 224)


_model = None
_class_names = None


def load_resources():

    global _model
    global _class_names

    if _model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Disease model not found:\n{MODEL_PATH}"
            )

        _model = load_model(
            MODEL_PATH
        )

    if _class_names is None:

        if not os.path.exists(CLASS_NAMES_PATH):
            raise FileNotFoundError(
                f"Class names file not found:\n{CLASS_NAMES_PATH}"
            )

        with open(
            CLASS_NAMES_PATH,
            "r"
        ) as f:

            _class_names = json.load(f)


def extract_crop_name(class_name):

    if "___" in class_name:

        crop = class_name.split(
            "___",
            1
        )[0]

    else:

        crop = class_name

    return crop.replace(
        "_",
        " "
    ).replace(
        ",",
        ", "
    )


def is_healthy(class_name):

    return "healthy" in class_name.lower()


def predict_disease(image_path):

    load_resources()

    if not os.path.exists(image_path):

        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )

    image = load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    image_array = img_to_array(
        image
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    predictions = _model.predict(
        image_array,
        verbose=0
    )[0]

    top_indices = np.argsort(
        predictions
    )[::-1][:3]

    top_predictions = []

    for index in top_indices:

        class_name = _class_names[
            int(index)
        ]

        confidence = (
            float(predictions[index])
            * 100
        )

        top_predictions.append(
            {
                "class": class_name,
                "crop": extract_crop_name(
                    class_name
                ),
                "confidence": round(
                    confidence,
                    2
                ),
                "healthy": is_healthy(
                    class_name
                )
            }
        )

    best_index = int(
        top_indices[0]
    )

    predicted_class = _class_names[
        best_index
    ]

    confidence = (
        float(predictions[best_index])
        * 100
    )

    crop = extract_crop_name(
        predicted_class
    )

    healthy = is_healthy(
        predicted_class
    )

    if healthy:

        status = "Healthy"

    else:

        status = "Disease Detected"

    return {
        "crop": crop,
        "disease": predicted_class,
        "confidence": round(
            confidence,
            2
        ),
        "status": status,
        "healthy": healthy,
        "top_predictions": top_predictions
    }