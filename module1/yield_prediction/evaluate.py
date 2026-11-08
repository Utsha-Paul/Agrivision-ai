import os
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from tensorflow.keras.models import load_model

from preprocessing import load_data, prepare_data


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "module1",
    "raw",
    "farm_data.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "module1",
    "crop_yield_mlp.keras"
)


def main():

    df = load_data(DATA_PATH)

    X_train, X_test, y_train, y_test = prepare_data(df)

    model = load_model(MODEL_PATH)

    predictions = model.predict(
        X_test,
        verbose=0
    ).flatten()

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    print("\n===== MODULE 1 EVALUATION =====")

    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")


if __name__ == "__main__":
    main()