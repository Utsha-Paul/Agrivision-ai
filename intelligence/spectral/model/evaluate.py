import os
import sys
import json

import joblib
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# PROJECT ROOT
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            CURRENT_DIR
        )
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(
        0,
        BASE_DIR
    )


# ============================================================
# IMPORT DATASET
# ============================================================

from intelligence.spectral.model.dataset import (
    build_dataset,
    load_cached_dataset,
    save_dataset_cache,
    TARGET_COLUMNS
)


# ============================================================
# PATHS
# ============================================================

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "spectral"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "spectral"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "hyperleaf_spectral.keras"
)

FEATURE_SCALER_PATH = os.path.join(
    MODEL_DIR,
    "hyperleaf_feature_scaler.pkl"
)

TARGET_SCALER_PATH = os.path.join(
    MODEL_DIR,
    "hyperleaf_target_scaler.pkl"
)

METRICS_PATH = os.path.join(
    OUTPUT_DIR,
    "hyperleaf_evaluation.json"
)


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42
TEST_SIZE = 0.20


# ============================================================
# CHECK FILES
# ============================================================

def check_files():

    required_files = [
        MODEL_PATH,
        FEATURE_SCALER_PATH,
        TARGET_SCALER_PATH
    ]

    for path in required_files:

        if not os.path.exists(path):

            raise FileNotFoundError(
                "\nRequired file not found:\n"
                f"{path}\n\n"
                "Make sure train.py completed successfully."
            )


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print(
        "\nLoading HyperLeaf dataset..."
    )

    X, y = load_cached_dataset()

    if X is None or y is None:

        print(
            "\nCached dataset not found."
        )

        print(
            "Building dataset from TIFF images..."
        )

        X, y = build_dataset(
            verbose=True
        )

        save_dataset_cache(
            X,
            y
        )

    return X, y


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    print(
        "\n========================================"
    )

    print(
        "          AGRIVISION AI"
    )

    print(
        "     HYPERLEAF EVALUATION"
    )

    print(
        "========================================"
    )

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    print(
        "\n[1/6] Checking trained model..."
    )

    check_files()

    print(
        "All required model files found."
    )

    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    print(
        "\n[2/6] Loading dataset..."
    )

    X, y = load_dataset()

    print(
        f"Dataset shape: {X.shape}"
    )

    print(
        f"Target shape : {y.shape}"
    )

    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    print(
        "\n[3/6] Creating evaluation split..."
    )

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    print(
        f"Total samples : {len(X)}"
    )

    print(
        f"Test samples  : {len(X_test)}"
    )

    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    print(
        "\n[4/6] Loading scalers..."
    )

    feature_scaler = joblib.load(
        FEATURE_SCALER_PATH
    )

    target_scaler = joblib.load(
        TARGET_SCALER_PATH
    )

    X_test_scaled = feature_scaler.transform(
        X_test
    )

    print(
        "Scalers loaded successfully."
    )

    # --------------------------------------------------------
    # STEP 5
    # --------------------------------------------------------

    print(
        "\n[5/6] Loading trained model..."
    )

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print(
        "Model loaded successfully."
    )

    print(
        "\nGenerating predictions..."
    )

    predictions_scaled = model.predict(
        X_test_scaled,
        verbose=1
    )

    predictions = target_scaler.inverse_transform(
        predictions_scaled
    )

    predictions = np.nan_to_num(
        predictions,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )

    # --------------------------------------------------------
    # STEP 6
    # --------------------------------------------------------

    print(
        "\n[6/6] Calculating metrics..."
    )

    results = {}

    print(
        "\n========================================"
    )

    print(
        "       HYPERLEAF EVALUATION RESULTS"
    )

    print(
        "========================================"
    )

    for index, target in enumerate(
        TARGET_COLUMNS
    ):

        actual = y_test[
            :,
            index
        ]

        predicted = predictions[
            :,
            index
        ]

        mae = mean_absolute_error(
            actual,
            predicted
        )

        rmse = np.sqrt(
            mean_squared_error(
                actual,
                predicted
            )
        )

        r2 = r2_score(
            actual,
            predicted
        )

        results[target] = {
            "mae": float(
                mae
            ),
            "rmse": float(
                rmse
            ),
            "r2": float(
                r2
            )
        }

        print(
            f"\n{target}"
        )

        print(
            f"MAE  : {mae:.6f}"
        )

        print(
            f"RMSE : {rmse:.6f}"
        )

        print(
            f"R²   : {r2:.6f}"
        )

    # --------------------------------------------------------
    # OVERALL METRICS
    # --------------------------------------------------------

    overall_mae = mean_absolute_error(
        y_test,
        predictions
    )

    overall_rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    overall_r2 = r2_score(
        y_test,
        predictions,
        multioutput="uniform_average"
    )

    results["overall"] = {
        "mae": float(
            overall_mae
        ),
        "rmse": float(
            overall_rmse
        ),
        "r2": float(
            overall_r2
        )
    }

    print(
        "\n----------------------------------------"
    )

    print(
        "OVERALL"
    )

    print(
        f"MAE  : {overall_mae:.6f}"
    )

    print(
        f"RMSE : {overall_rmse:.6f}"
    )

    print(
        f"R²   : {overall_r2:.6f}"
    )

    # --------------------------------------------------------
    # SAMPLE PREDICTIONS
    # --------------------------------------------------------

    print(
        "\n========================================"
    )

    print(
        "        SAMPLE PREDICTIONS"
    )

    print(
        "========================================"
    )

    sample_count = min(
        10,
        len(y_test)
    )

    for i in range(
        sample_count
    ):

        print(
            f"\nSample {i + 1}"
        )

        for j, target in enumerate(
            TARGET_COLUMNS
        ):

            print(
                f"{target:<12}"
                f" Actual: "
                f"{y_test[i, j]:.6f}"
                f" | Predicted: "
                f"{predictions[i, j]:.6f}"
            )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    evaluation_data = {

        "model": (
            "AgriVision "
            "HyperLeaf Spectral Model"
        ),

        "dataset": "HyperLeaf2024",

        "total_samples": int(
            len(X)
        ),

        "test_samples": int(
            len(X_test)
        ),

        "spectral_bands": int(
            X.shape[1]
        ),

        "targets": TARGET_COLUMNS,

        "test_size": TEST_SIZE,

        "random_state": RANDOM_STATE,

        "metrics": results
    }

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    with open(
        METRICS_PATH,
        "w"
    ) as file:

        json.dump(
            evaluation_data,
            file,
            indent=4
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

    print(
        "\nMetrics saved to:"
    )

    print(
        METRICS_PATH
    )

    print(
        "\n========================================"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()