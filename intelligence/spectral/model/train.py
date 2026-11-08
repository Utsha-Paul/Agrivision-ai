import os
import sys
import json

import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import tensorflow as tf
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
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
# IMPORTS
# ============================================================

from intelligence.spectral.model.dataset import (
    build_dataset,
    load_cached_dataset,
    save_dataset_cache,
    TARGET_COLUMNS
)

from intelligence.spectral.model.model import (
    build_spectral_model
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
    "hyperleaf_metrics.json"
)

HISTORY_PATH = os.path.join(
    OUTPUT_DIR,
    "hyperleaf_training_history.json"
)


# ============================================================
# TRAINING CONFIGURATION
# ============================================================

RANDOM_STATE = 42

VALIDATION_SIZE = 0.20

EPOCHS = 100

BATCH_SIZE = 32


# ============================================================
# CREATE DIRECTORIES
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n========================================"
    )

    print(
        "          AGRIVISION AI"
    )

    print(
        "       HYPERLEAF TRAINING"
    )

    print(
        "========================================"
    )

    # --------------------------------------------------------
    # STEP 1: LOAD / BUILD DATASET
    # --------------------------------------------------------

    print(
        "\n[1/7] Loading spectral dataset..."
    )

    X, y = load_cached_dataset()

    if X is None or y is None:

        print(
            "\nNo cached dataset found."
        )

        print(
            "Processing HyperLeaf TIFF images..."
        )

        X, y = build_dataset(
            verbose=True
        )

        print(
            "\nSaving processed dataset..."
        )

        save_dataset_cache(
            X,
            y
        )

    else:

        print(
            "Using cached spectral features."
        )

    # --------------------------------------------------------
    # DATASET VALIDATION
    # --------------------------------------------------------

    if len(X) == 0:

        raise RuntimeError(
            "Dataset contains no samples."
        )

    if len(X) != len(y):

        raise ValueError(
            "Feature and target sample counts "
            "do not match."
        )

    print(
        "\nDataset information:"
    )

    print(
        f"Samples : {len(X)}"
    )

    print(
        f"Features: {X.shape[1]}"
    )

    print(
        f"Targets : {y.shape[1]}"
    )

    print(
        "\nTargets:"
    )

    for target in TARGET_COLUMNS:

        print(
            f"  - {target}"
        )

    # --------------------------------------------------------
    # STEP 2: TRAIN / VALIDATION SPLIT
    # --------------------------------------------------------

    print(
        "\n[2/7] Creating train/validation split..."
    )

    (
        X_train,
        X_val,
        y_train,
        y_val
    ) = train_test_split(
        X,
        y,
        test_size=VALIDATION_SIZE,
        random_state=RANDOM_STATE
    )

    print(
        f"Training samples  : {len(X_train)}"
    )

    print(
        f"Validation samples: {len(X_val)}"
    )

    # --------------------------------------------------------
    # STEP 3: FEATURE SCALING
    # --------------------------------------------------------

    print(
        "\n[3/7] Scaling spectral features..."
    )

    feature_scaler = StandardScaler()

    X_train_scaled = feature_scaler.fit_transform(
        X_train
    )

    X_val_scaled = feature_scaler.transform(
        X_val
    )

    # --------------------------------------------------------
    # TARGET SCALING
    # --------------------------------------------------------

    print(
        "Scaling target values..."
    )

    target_scaler = StandardScaler()

    y_train_scaled = target_scaler.fit_transform(
        y_train
    )

    y_val_scaled = target_scaler.transform(
        y_val
    )

    # --------------------------------------------------------
    # SAVE SCALERS
    # --------------------------------------------------------

    joblib.dump(
        feature_scaler,
        FEATURE_SCALER_PATH
    )

    joblib.dump(
        target_scaler,
        TARGET_SCALER_PATH
    )

    print(
        "\nFeature scaler saved:"
    )

    print(
        FEATURE_SCALER_PATH
    )

    print(
        "\nTarget scaler saved:"
    )

    print(
        TARGET_SCALER_PATH
    )

    # --------------------------------------------------------
    # STEP 4: BUILD MODEL
    # --------------------------------------------------------

    print(
        "\n[4/7] Building spectral model..."
    )

    model = build_spectral_model(
        input_bands=X_train_scaled.shape[1]
    )

    print(
        "\nModel architecture:"
    )

    model.summary()

    # --------------------------------------------------------
    # CALLBACKS
    # --------------------------------------------------------

    checkpoint = ModelCheckpoint(
        MODEL_PATH,
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    )

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=15,
        restore_best_weights=True,
        verbose=1
    )

    reduce_lr = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=6,
        min_lr=1e-6,
        verbose=1
    )

    # --------------------------------------------------------
    # STEP 5: TRAIN
    # --------------------------------------------------------

    print(
        "\n[5/7] Starting training..."
    )

    print(
        f"\nEpochs    : {EPOCHS}"
    )

    print(
        f"Batch size: {BATCH_SIZE}"
    )

    history = model.fit(
        X_train_scaled,
        y_train_scaled,
        validation_data=(
            X_val_scaled,
            y_val_scaled
        ),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[
            checkpoint,
            early_stopping,
            reduce_lr
        ],
        verbose=1
    )

    # --------------------------------------------------------
    # STEP 6: LOAD BEST MODEL
    # --------------------------------------------------------

    print(
        "\n[6/7] Loading best model..."
    )

    best_model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print(
        "Best model loaded successfully."
    )

    # --------------------------------------------------------
    # PREDICTIONS
    # --------------------------------------------------------

    print(
        "\nGenerating validation predictions..."
    )

    predictions_scaled = best_model.predict(
        X_val_scaled,
        verbose=1
    )

    # --------------------------------------------------------
    # INVERSE TARGET SCALING
    # --------------------------------------------------------

    predictions = target_scaler.inverse_transform(
        predictions_scaled
    )

    actual = y_val

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    metrics = {}

    print(
        "\n========================================"
    )

    print(
        "       HYPERLEAF VALIDATION RESULTS"
    )

    print(
        "========================================"
    )

    for index, target in enumerate(
        TARGET_COLUMNS
    ):

        actual_target = actual[
            :, index
        ]

        predicted_target = predictions[
            :, index
        ]

        mae = mean_absolute_error(
            actual_target,
            predicted_target
        )

        rmse = np.sqrt(
            mean_squared_error(
                actual_target,
                predicted_target
            )
        )

        r2 = r2_score(
            actual_target,
            predicted_target
        )

        metrics[target] = {
            "mae": float(mae),
            "rmse": float(rmse),
            "r2": float(r2)
        }

        print(
            f"\n{target}"
        )

        print(
            f"  MAE  : {mae:.6f}"
        )

        print(
            f"  RMSE : {rmse:.6f}"
        )

        print(
            f"  R2   : {r2:.6f}"
        )

    # --------------------------------------------------------
    # OVERALL METRICS
    # --------------------------------------------------------

    overall_mae = mean_absolute_error(
        actual,
        predictions
    )

    overall_rmse = np.sqrt(
        mean_squared_error(
            actual,
            predictions
        )
    )

    overall_r2 = r2_score(
        actual,
        predictions,
        multioutput="uniform_average"
    )

    metrics["overall"] = {
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
        "Overall"
    )

    print(
        f"  MAE  : {overall_mae:.6f}"
    )

    print(
        f"  RMSE : {overall_rmse:.6f}"
    )

    print(
        f"  R2   : {overall_r2:.6f}"
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

    samples_to_show = min(
        5,
        len(actual)
    )

    for i in range(
        samples_to_show
    ):

        print(
            f"\nSample {i + 1}"
        )

        for j, target in enumerate(
            TARGET_COLUMNS
        ):

            print(
                f"  {target:<12} "
                f"Actual: "
                f"{actual[i, j]:.6f}  |  "
                f"Predicted: "
                f"{predictions[i, j]:.6f}"
            )

    # --------------------------------------------------------
    # SAVE METRICS
    # --------------------------------------------------------

    print(
        "\n[7/7] Saving training results..."
    )

    training_metrics = {
        "model": "AgriVision HyperLeaf Spectral Model",
        "dataset": "HyperLeaf2024",
        "samples": int(
            len(X)
        ),
        "training_samples": int(
            len(X_train)
        ),
        "validation_samples": int(
            len(X_val)
        ),
        "spectral_bands": int(
            X.shape[1]
        ),
        "targets": TARGET_COLUMNS,
        "epochs_requested": EPOCHS,
        "epochs_completed": len(
            history.history[
                "loss"
            ]
        ),
        "batch_size": BATCH_SIZE,
        "validation_size": VALIDATION_SIZE,
        "metrics": metrics
    }

    with open(
        METRICS_PATH,
        "w"
    ) as file:

        json.dump(
            training_metrics,
            file,
            indent=4
        )

    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    history_data = {}

    for key, values in history.history.items():

        history_data[key] = [
            float(value)
            for value in values
        ]

    with open(
        HISTORY_PATH,
        "w"
    ) as file:

        json.dump(
            history_data,
            file,
            indent=4
        )

    # --------------------------------------------------------
    # FINAL INFORMATION
    # --------------------------------------------------------

    print(
        "\n========================================"
    )

    print(
        "        TRAINING COMPLETED"
    )

    print(
        "========================================"
    )

    print(
        "\nModel:"
    )

    print(
        MODEL_PATH
    )

    print(
        "\nFeature scaler:"
    )

    print(
        FEATURE_SCALER_PATH
    )

    print(
        "\nTarget scaler:"
    )

    print(
        TARGET_SCALER_PATH
    )

    print(
        "\nMetrics:"
    )

    print(
        METRICS_PATH
    )

    print(
        "\nTraining history:"
    )

    print(
        HISTORY_PATH
    )

    print(
        "\n========================================"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()