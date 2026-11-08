import os
import sys

# ============================================================
# PROJECT ROOT
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        CURRENT_DIR
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# IMPORTS
# ============================================================

import numpy as np
import joblib

try:
    from keras.models import load_model
except ImportError:
    from tensorflow.keras.models import load_model

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from intelligence.forecasting.dataset import (
    load_dataset,
    prepare_sequences,
    SEQUENCE_LENGTH,
    TARGET
)


# ============================================================
# PATHS
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "forecasting",
    "crop_yield_lstm.keras"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "forecasting",
    "lstm_scaler.pkl"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n========================================")
    print("          AGRIVISION AI")
    print("        LSTM EVALUATION")
    print("========================================")

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            f"\nLSTM model not found:\n"
            f"{MODEL_PATH}\n\n"
            f"Train the model first."
        )

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    print("\nLoading LSTM model...")

    model = load_model(
        MODEL_PATH
    )

    print(
        "Model loaded successfully."
    )

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    print(
        "\nLoading dataset..."
    )

    df = load_dataset()

    # --------------------------------------------------------
    # CREATE SAME SEQUENCES
    # --------------------------------------------------------

    print(
        "\nCreating evaluation sequences..."
    )

    X, y, scaler = prepare_sequences(
        df,
        sequence_length=SEQUENCE_LENGTH
    )

    # --------------------------------------------------------
    # TEMPORAL TEST SPLIT
    # --------------------------------------------------------

    split_index = int(
        len(X) * 0.8
    )

    X_test = X[
        split_index:
    ]

    y_test = y[
        split_index:
    ]

    print(
        f"\nTotal sequences: {len(X)}"
    )

    print(
        f"Test sequences: {len(X_test)}"
    )

    # --------------------------------------------------------
    # PREDICTIONS
    # --------------------------------------------------------

    print(
        "\nGenerating predictions..."
    )

    predictions_scaled = model.predict(
        X_test,
        verbose=1
    ).flatten()

    # --------------------------------------------------------
    # CONVERT BACK TO KG/HA
    # --------------------------------------------------------

    target_index = (
        scaler.feature_names_in_.tolist()
        .index(TARGET)
    )

    target_mean = scaler.mean_[
        target_index
    ]

    target_scale = scaler.scale_[
        target_index
    ]

    predictions = (
        predictions_scaled
        * target_scale
        + target_mean
    )

    actual = (
        y_test
        * target_scale
        + target_mean
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    mae = mean_absolute_error(
        actual,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predictions
        )
    )

    r2 = r2_score(
        actual,
        predictions
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    print(
        "\n========================================"
    )

    print(
        "       LSTM EVALUATION RESULTS"
    )

    print(
        "========================================"
    )

    print(
        f"\nMAE  : {mae:.2f} kg/ha"
    )

    print(
        f"RMSE : {rmse:.2f} kg/ha"
    )

    print(
        f"R²   : {r2:.4f}"
    )

    print(
        "\n========================================"
    )

    print(
        "Sample Predictions"
    )

    print(
        "========================================"
    )

    number_of_samples = min(
        10,
        len(actual)
    )

    for i in range(
        number_of_samples
    ):

        print(
            f"{i + 1:02d}. "
            f"Actual: "
            f"{actual[i]:.2f} kg/ha   |   "
            f"Predicted: "
            f"{predictions[i]:.2f} kg/ha"
        )

    # --------------------------------------------------------
    # SAVE METRICS
    # --------------------------------------------------------

    output_dir = os.path.join(
        BASE_DIR,
        "outputs",
        "forecasting"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    metrics_path = os.path.join(
        output_dir,
        "lstm_metrics.json"
    )

    import json

    metrics = {
        "model": "LSTM",
        "target": TARGET,
        "sequence_length": SEQUENCE_LENGTH,
        "test_samples": int(
            len(X_test)
        ),
        "mae_kg_per_ha": float(
            mae
        ),
        "rmse_kg_per_ha": float(
            rmse
        ),
        "r2": float(
            r2
        )
    }

    with open(
        metrics_path,
        "w"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )

    print(
        "\nMetrics saved to:"
    )

    print(
        metrics_path
    )

    print(
        "\n========================================"
    )

    print(
        "       EVALUATION COMPLETED"
    )

    print(
        "========================================"
    )


if __name__ == "__main__":
    main()