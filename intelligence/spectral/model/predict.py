import os

import joblib
import numpy as np
import tifffile

try:
    from keras.models import load_model
except ImportError:
    from tensorflow.keras.models import load_model


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


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
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


# ============================================================
# HYPERLEAF CONFIGURATION
# ============================================================

EXPECTED_SPECTRAL_BANDS = 204

TARGET_NAMES = [
    "GrainWeight",
    "Gsw",
    "PhiPS2"
]


# ============================================================
# RESOURCE CACHE
# ============================================================

_model = None
_feature_scaler = None
_target_scaler = None


# ============================================================
# LOAD MODEL RESOURCES
# ============================================================

def load_resources():

    global _model
    global _feature_scaler
    global _target_scaler

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not os.path.exists(
        MODEL_PATH
    ):

        raise FileNotFoundError(
            "\nSpectral model not found:\n"
            f"{MODEL_PATH}\n\n"
            "Run train.py first."
        )

    if not os.path.exists(
        FEATURE_SCALER_PATH
    ):

        raise FileNotFoundError(
            "\nFeature scaler not found:\n"
            f"{FEATURE_SCALER_PATH}\n\n"
            "Run train.py first."
        )

    if not os.path.exists(
        TARGET_SCALER_PATH
    ):

        raise FileNotFoundError(
            "\nTarget scaler not found:\n"
            f"{TARGET_SCALER_PATH}\n\n"
            "Run train.py first."
        )

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    if _model is None:

        print(
            "\nLoading HyperLeaf spectral model..."
        )

        _model = load_model(
            MODEL_PATH
        )

    # --------------------------------------------------------
    # Load feature scaler
    # --------------------------------------------------------

    if _feature_scaler is None:

        _feature_scaler = joblib.load(
            FEATURE_SCALER_PATH
        )

    # --------------------------------------------------------
    # Load target scaler
    # --------------------------------------------------------

    if _target_scaler is None:

        _target_scaler = joblib.load(
            TARGET_SCALER_PATH
        )


# ============================================================
# LOAD HYPERSPECTRAL IMAGE
# ============================================================

def load_hyperspectral_image(
    image_path
):

    if not image_path:

        raise ValueError(
            "Image path cannot be empty."
        )

    if not os.path.exists(
        image_path
    ):

        raise FileNotFoundError(
            f"\nHyperspectral image not found:\n"
            f"{image_path}"
        )

    # --------------------------------------------------------
    # Read TIFF
    # --------------------------------------------------------

    cube = tifffile.imread(
        image_path
    )

    cube = np.asarray(
        cube
    )

    if cube.ndim != 3:

        raise ValueError(
            "\nInvalid hyperspectral image.\n"
            f"Expected 3 dimensions, "
            f"received: {cube.shape}"
        )

    # --------------------------------------------------------
    # Detect spectral axis
    # --------------------------------------------------------

    spectral_axes = [
        index
        for index, size
        in enumerate(
            cube.shape
        )
        if size == EXPECTED_SPECTRAL_BANDS
    ]

    if not spectral_axes:

        raise ValueError(
            "\nCould not find the "
            f"{EXPECTED_SPECTRAL_BANDS}-band spectral axis.\n"
            f"Image shape: {cube.shape}"
        )

    spectral_axis = spectral_axes[0]

    # --------------------------------------------------------
    # Move spectral axis to last position
    # --------------------------------------------------------

    cube = np.moveaxis(
        cube,
        spectral_axis,
        -1
    )

    return cube.astype(
        np.float32
    )


# ============================================================
# EXTRACT SPECTRAL SIGNATURE
# ============================================================

def extract_spectral_signature(
    cube
):

    cube = np.asarray(
        cube,
        dtype=np.float32
    )

    if cube.ndim != 3:

        raise ValueError(
            f"Expected 3D cube, "
            f"received {cube.shape}"
        )

    height, width, bands = cube.shape

    if bands != EXPECTED_SPECTRAL_BANDS:

        raise ValueError(
            f"Expected "
            f"{EXPECTED_SPECTRAL_BANDS} spectral bands, "
            f"received {bands}."
        )

    # --------------------------------------------------------
    # Detect leaf pixels
    # --------------------------------------------------------

    pixel_energy = np.sum(
        np.abs(cube),
        axis=2
    )

    mask = (
        pixel_energy > 0
    )

    if not np.any(mask):

        raise ValueError(
            "No valid leaf pixels were detected "
            "in the hyperspectral image."
        )

    # --------------------------------------------------------
    # Extract leaf pixels
    # --------------------------------------------------------

    leaf_pixels = cube[
        mask
    ]

    # --------------------------------------------------------
    # Mean spectral signature
    # --------------------------------------------------------

    spectral_signature = np.mean(
        leaf_pixels,
        axis=0
    )

    # --------------------------------------------------------
    # Clean values
    # --------------------------------------------------------

    spectral_signature = np.nan_to_num(
        spectral_signature,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )

    return spectral_signature.astype(
        np.float32
    )


# ============================================================
# PREDICT FROM SPECTRAL SIGNATURE
# ============================================================

def predict_from_signature(
    spectral_signature
):

    load_resources()

    spectral_signature = np.asarray(
        spectral_signature,
        dtype=np.float32
    )

    if spectral_signature.shape != (
        EXPECTED_SPECTRAL_BANDS,
    ):

        raise ValueError(
            "\nInvalid spectral signature shape.\n"
            f"Expected: "
            f"({EXPECTED_SPECTRAL_BANDS},)\n"
            f"Received: "
            f"{spectral_signature.shape}"
        )

    # --------------------------------------------------------
    # Add batch dimension
    # --------------------------------------------------------

    features = spectral_signature.reshape(
        1,
        -1
    )

    # --------------------------------------------------------
    # Feature scaling
    # --------------------------------------------------------

    features_scaled = _feature_scaler.transform(
        features
    )

    # --------------------------------------------------------
    # Model prediction
    # --------------------------------------------------------

    prediction_scaled = _model.predict(
        features_scaled,
        verbose=0
    )

    # --------------------------------------------------------
    # Reverse target scaling
    # --------------------------------------------------------

    prediction = _target_scaler.inverse_transform(
        prediction_scaled
    )[0]

    prediction = np.asarray(
        prediction,
        dtype=np.float64
    )

    prediction = np.nan_to_num(
        prediction,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )

    return prediction


# ============================================================
# PREDICT FROM TIFF
# ============================================================

def predict_spectral(
    image_path
):

    """
    Complete HyperLeaf prediction pipeline.

    Input:
        Hyperspectral TIFF

    Output:
        GrainWeight
        Gsw
        PhiPS2
    """

    # --------------------------------------------------------
    # Load image
    # --------------------------------------------------------

    cube = load_hyperspectral_image(
        image_path
    )

    # --------------------------------------------------------
    # Extract spectral signature
    # --------------------------------------------------------

    spectral_signature = extract_spectral_signature(
        cube
    )

    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    prediction = predict_from_signature(
        spectral_signature
    )

    result = {

        "image_path": os.path.abspath(
            image_path
        ),

        "spectral_bands": EXPECTED_SPECTRAL_BANDS,

        "grain_weight": float(
            prediction[0]
        ),

        "gsw": float(
            prediction[1]
        ),

        "phi_ps2": float(
            prediction[2]
        )
    }

    return result


# ============================================================
# HUMAN-READABLE RESULT
# ============================================================

def print_prediction(
    result
):

    print(
        "\n========================================"
    )

    print(
        "       AGRIVISION AI"
    )

    print(
        "    SPECTRAL PREDICTION"
    )

    print(
        "========================================"
    )

    print(
        f"\nImage:"
    )

    print(
        result[
            "image_path"
        ]
    )

    print(
        f"\nSpectral bands:"
        f" {result['spectral_bands']}"
    )

    print(
        "\n----------------------------------------"
    )

    print(
        "HYPERLEAF PREDICTIONS"
    )

    print(
        "----------------------------------------"
    )

    print(
        f"\nGrainWeight:"
        f" {result['grain_weight']:.4f}"
    )

    print(
        f"Gsw:"
        f" {result['gsw']:.6f}"
    )

    print(
        f"PhiPS2:"
        f" {result['phi_ps2']:.6f}"
    )

    print(
        "\n========================================"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "      HYPERLEAF MODEL TEST"
    )

    print(
        "========================================"
    )

    # --------------------------------------------------------
    # Automatically use HyperLeaf 00000.tiff
    # --------------------------------------------------------

    image_path = os.path.join(
        BASE_DIR,
        "data",
        "spectral",
        "HyperLeaf2024",
        "images",
        "00000.tiff"
    )

    if not os.path.exists(
        image_path
    ):

        # Try .tif
        alternative_path = os.path.join(
            BASE_DIR,
            "data",
            "spectral",
            "HyperLeaf2024",
            "images",
            "00000.tif"
        )

        if os.path.exists(
            alternative_path
        ):

            image_path = alternative_path

    print(
        "\nTest image:"
    )

    print(
        image_path
    )

    result = predict_spectral(
        image_path
    )

    print_prediction(
        result
    )

    print(
        "\nSpectral prediction test completed."
    )