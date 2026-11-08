import os
import joblib
import pandas as pd

try:
    from keras.models import load_model
except ImportError:
    from tensorflow.keras.models import load_model


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
    "module1",
    "crop_yield_mlp.keras"
)

PREPROCESSOR_PATH = os.path.join(
    BASE_DIR,
    "models",
    "module1",
    "preprocessor.pkl"
)

_model = None
_preprocessor = None


def load_resources():
    global _model
    global _preprocessor

    if _model is None:
        _model = load_model(MODEL_PATH)

    if _preprocessor is None:
        _preprocessor = joblib.load(PREPROCESSOR_PATH)


def predict_crop_yield(
    rainfall_mm,
    avg_temp_c,
    humidity_pct,
    soil_ph,
    nitrogen_kg_ha,
    phosphorus_kg_ha,
    potassium_kg_ha,
    irrigation_mm,
    days_from_last_harvest,
    pest_index,
    soil_type,
    crop_type,
    fertilized,
    weather_zone,
    seed_quality,
    irrigation_method,
    season
):

    load_resources()

    data = pd.DataFrame([{
        "rainfall_mm": rainfall_mm,
        "avg_temp_c": avg_temp_c,
        "humidity_pct": humidity_pct,
        "soil_ph": soil_ph,
        "nitrogen_kg_ha": nitrogen_kg_ha,
        "phosphorus_kg_ha": phosphorus_kg_ha,
        "potassium_kg_ha": potassium_kg_ha,
        "irrigation_mm": irrigation_mm,
        "days_from_last_harvest": days_from_last_harvest,
        "pest_index": pest_index,
        "soil_type": soil_type,
        "crop_type": crop_type,
        "fertilized": fertilized,
        "weather_zone": weather_zone,
        "seed_quality": seed_quality,
        "irrigation_method": irrigation_method,
        "season": season
    }])

    data = _preprocessor.transform(data)

    prediction = _model.predict(
        data,
        verbose=0
    )[0][0]

    return float(prediction)