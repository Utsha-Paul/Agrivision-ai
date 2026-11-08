import tensorflow as tf
from tensorflow.keras import layers, models


# ============================================================
# MODEL CONFIGURATION
# ============================================================

INPUT_BANDS = 204
OUTPUT_TARGETS = 3


# ============================================================
# BUILD SPECTRAL MODEL
# ============================================================

def build_spectral_model(
    input_bands=INPUT_BANDS
):
    """
    Build a lightweight neural network for
    hyperspectral spectral regression.

    Input:
        204 spectral bands

    Outputs:
        GrainWeight
        Gsw
        PhiPS2
    """

    inputs = layers.Input(
        shape=(input_bands,),
        name="spectral_input"
    )

    # --------------------------------------------------------
    # Normalize spectral features
    # --------------------------------------------------------

    x = layers.BatchNormalization(
        name="spectral_normalization"
    )(inputs)

    # --------------------------------------------------------
    # Spectral feature extraction
    # --------------------------------------------------------

    x = layers.Dense(
        256,
        activation="relu",
        name="spectral_dense_1"
    )(x)

    x = layers.BatchNormalization(
        name="spectral_bn_1"
    )(x)

    x = layers.Dropout(
        0.25,
        name="spectral_dropout_1"
    )(x)

    x = layers.Dense(
        128,
        activation="relu",
        name="spectral_dense_2"
    )(x)

    x = layers.BatchNormalization(
        name="spectral_bn_2"
    )(x)

    x = layers.Dropout(
        0.20,
        name="spectral_dropout_2"
    )(x)

    x = layers.Dense(
        64,
        activation="relu",
        name="spectral_dense_3"
    )(x)

    # --------------------------------------------------------
    # Shared spectral representation
    # --------------------------------------------------------

    x = layers.Dense(
        32,
        activation="relu",
        name="spectral_embedding"
    )(x)

    # --------------------------------------------------------
    # Regression output
    # --------------------------------------------------------

    outputs = layers.Dense(
        OUTPUT_TARGETS,
        activation="linear",
        name="spectral_targets"
    )(x)

    model = models.Model(
        inputs=inputs,
        outputs=outputs,
        name="AgriVision_HyperLeaf_Spectral_Model"
    )

    # --------------------------------------------------------
    # Compile
    # --------------------------------------------------------

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="mse",
        metrics=[
            tf.keras.metrics.MeanAbsoluteError(
                name="mae"
            )
        ]
    )

    return model


# ============================================================
# TEST MODEL
# ============================================================

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "     AGRIVISION AI SPECTRAL MODEL"
    )

    print(
        "========================================"
    )

    model = build_spectral_model()

    model.summary()

    print(
        "\nModel created successfully."
    )

    print(
        f"Input bands : {INPUT_BANDS}"
    )

    print(
        f"Outputs     : {OUTPUT_TARGETS}"
    )

    print(
        "\nTargets:"
    )

    print(
        "1. GrainWeight"
    )

    print(
        "2. Gsw"
    )

    print(
        "3. PhiPS2"
    )

    print(
        "\n========================================"
    )