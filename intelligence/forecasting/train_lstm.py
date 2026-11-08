import os
import sys

# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
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
    sys.path.insert(
        0,
        BASE_DIR
    )


# ============================================================
# IMPORTS
# ============================================================

import tensorflow as tf
from sklearn.model_selection import train_test_split

from intelligence.forecasting.dataset import (
    load_dataset,
    prepare_sequences,
    SEQUENCE_LENGTH
)

from intelligence.forecasting.lstm_model import (
    build_lstm_model
)


# ============================================================
# MODEL PATH
# ============================================================

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "forecasting"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "crop_yield_lstm.keras"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n========================================")
    print("          AGRIVISION AI")
    print("        LSTM FORECASTING")
    print("========================================")

    # --------------------------------------------------------
    # CREATE MODEL DIRECTORY
    # --------------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    # --------------------------------------------------------
    # LOAD DATASET
    # --------------------------------------------------------

    print(
        "\nLoading dataset..."
    )

    df = load_dataset()

    # --------------------------------------------------------
    # CREATE SEQUENCES
    # --------------------------------------------------------

    print(
        "\nCreating temporal sequences..."
    )

    X, y, scaler = prepare_sequences(
        df,
        sequence_length=SEQUENCE_LENGTH
    )

    if len(X) == 0:

        raise ValueError(
            "No sequences were created.\n"
            "Check the dataset structure."
        )

    print(
        f"\nX shape: {X.shape}"
    )

    print(
        f"y shape: {y.shape}"
    )

    # --------------------------------------------------------
    # TRAIN / TEST SPLIT
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            shuffle=False
        )
    )

    print(
        f"\nTraining samples: "
        f"{len(X_train)}"
    )

    print(
        f"Testing samples: "
        f"{len(X_test)}"
    )

    # --------------------------------------------------------
    # BUILD MODEL
    # --------------------------------------------------------

    print(
        "\nBuilding LSTM model..."
    )

    model = build_lstm_model(
        sequence_length=X.shape[1],
        num_features=X.shape[2]
    )

    print(
        "\nModel architecture:"
    )

    model.summary()

    # --------------------------------------------------------
    # CALLBACKS
    # --------------------------------------------------------

    callbacks = [

        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=10,
            restore_best_weights=True
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=5,
            min_lr=1e-6
        )
    ]

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    print(
        "\n========================================"
    )

    print(
        "STARTING LSTM TRAINING"
    )

    print(
        "========================================\n"
    )

    history = model.fit(
        X_train,
        y_train,
        validation_data=(
            X_test,
            y_test
        ),
        epochs=100,
        batch_size=64,
        callbacks=callbacks,
        verbose=1
    )

    # --------------------------------------------------------
    # SAVE MODEL
    # --------------------------------------------------------

    model.save(
        MODEL_PATH
    )

    print(
        "\n========================================"
    )

    print(
        "       LSTM TRAINING COMPLETED"
    )

    print(
        "========================================"
    )

    print(
        f"\nModel saved to:"
    )

    print(
        MODEL_PATH
    )

    print(
        f"\nFinal training loss: "
        f"{history.history['loss'][-1]:.6f}"
    )

    print(
        f"Final validation loss: "
        f"{history.history['val_loss'][-1]:.6f}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()