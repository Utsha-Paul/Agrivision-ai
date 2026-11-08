import os
import glob

import numpy as np
import pandas as pd
import tifffile


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
# FIND HYPERLEAF DATASET
# ============================================================

def find_dataset_dir():

    possible_paths = [

        # Recommended project location
        os.path.join(
            BASE_DIR,
            "data",
            "spectral",
            "HyperLeaf2024"
        ),

        # Windows Downloads
        os.path.join(
            os.path.expanduser("~"),
            "Downloads",
            "HyperLeaf2024"
        ),

        # One level above project
        os.path.join(
            os.path.dirname(BASE_DIR),
            "HyperLeaf2024"
        )
    ]

    for path in possible_paths:

        if (
            os.path.exists(path)
            and os.path.isdir(path)
        ):

            train_csv = os.path.join(
                path,
                "train.csv"
            )

            images_dir = os.path.join(
                path,
                "images"
            )

            if (
                os.path.exists(train_csv)
                and os.path.exists(images_dir)
            ):

                return path

    raise FileNotFoundError(
        "\nCould not locate HyperLeaf2024 dataset.\n\n"
        "Expected one of:\n\n"
        + "\n".join(
            possible_paths
        )
    )


DATASET_DIR = find_dataset_dir()

IMAGE_DIR = os.path.join(
    DATASET_DIR,
    "images"
)

TRAIN_CSV = os.path.join(
    DATASET_DIR,
    "train.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

TARGET_COLUMNS = [
    "GrainWeight",
    "Gsw",
    "PhiPS2"
]

EXPECTED_SPECTRAL_BANDS = 204


# ============================================================
# DATASET INFORMATION
# ============================================================

print(
    "\nHyperLeaf dataset found:"
)

print(
    DATASET_DIR
)

print(
    "\nImage directory:"
)

print(
    IMAGE_DIR
)


# ============================================================
# IMAGE RESOLUTION
# ============================================================

def find_image(image_id):

    """
    Resolve HyperLeaf ImageId to an actual TIFF file.

    Handles values such as:

        0
        0.0
        1
        1.0
        41
        41.0

    and filenames such as:

        00000.tif
        00001.tif
        00041.tif

    Also handles hidden TIFF extensions / uppercase extensions.
    """

    # --------------------------------------------------------
    # Convert ImageId safely
    # --------------------------------------------------------

    try:

        numeric_id = int(
            float(
                str(image_id).strip()
            )
        )

    except (
        ValueError,
        TypeError
    ):

        numeric_id = None

    candidate_names = []

    # --------------------------------------------------------
    # Standard HyperLeaf naming
    # --------------------------------------------------------

    if numeric_id is not None:

        candidate_names.extend([
            f"{numeric_id:05d}.tif",
            f"{numeric_id:05d}.TIF",
            f"{numeric_id:05d}.tiff",
            f"{numeric_id:05d}.TIFF",

            # Extensionless fallback
            f"{numeric_id:05d}"
        ])

    # --------------------------------------------------------
    # Original ImageId fallback
    # --------------------------------------------------------

    original_id = str(
        image_id
    ).strip()

    candidate_names.extend([
        f"{original_id}.tif",
        f"{original_id}.TIF",
        f"{original_id}.tiff",
        f"{original_id}.TIFF",
        original_id
    ])

    # --------------------------------------------------------
    # Direct lookup
    # --------------------------------------------------------

    for filename in candidate_names:

        path = os.path.join(
            IMAGE_DIR,
            filename
        )

        if os.path.isfile(path):

            return path

    # --------------------------------------------------------
    # Case-insensitive lookup
    # --------------------------------------------------------

    if numeric_id is not None:

        expected_stem = f"{numeric_id:05d}"

        try:

            for filename in os.listdir(
                IMAGE_DIR
            ):

                stem, extension = os.path.splitext(
                    filename
                )

                if (
                    stem.lower()
                    == expected_stem.lower()
                ):

                    path = os.path.join(
                        IMAGE_DIR,
                        filename
                    )

                    if os.path.isfile(path):

                        return path

        except FileNotFoundError:

            pass

    # --------------------------------------------------------
    # Recursive fallback
    # --------------------------------------------------------

    if numeric_id is not None:

        patterns = [
            f"**/{numeric_id:05d}.tif",
            f"**/{numeric_id:05d}.TIF",
            f"**/{numeric_id:05d}.tiff",
            f"**/{numeric_id:05d}.TIFF",
            f"**/{numeric_id:05d}"
        ]

        for pattern in patterns:

            matches = glob.glob(
                os.path.join(
                    IMAGE_DIR,
                    pattern
                ),
                recursive=True
            )

            if matches:

                return matches[0]

    # --------------------------------------------------------
    # Give useful error
    # --------------------------------------------------------

    sample_files = []

    try:

        sample_files = os.listdir(
            IMAGE_DIR
        )[:10]

    except Exception:

        pass

    raise FileNotFoundError(
        f"\nCould not find image for ImageId: "
        f"{image_id}\n\n"
        f"Expected filename similar to:\n"
        f"00000.tif\n\n"
        f"Image directory:\n"
        f"{IMAGE_DIR}\n\n"
        f"First files found:\n"
        f"{sample_files}"
    )


# ============================================================
# LOAD HYPERSPECTRAL TIFF
# ============================================================

def load_hyperspectral_image(
    image_path
):

    """
    Load a HyperLeaf hyperspectral TIFF.

    Expected dimensions are approximately:

        Height x Width x 204

    or

        204 x Height x Width

    The spectral axis is automatically detected.
    """

    cube = tifffile.imread(
        image_path
    )

    cube = np.asarray(
        cube
    )

    if cube.ndim != 3:

        raise ValueError(
            f"\nExpected a 3D hyperspectral cube.\n"
            f"Received shape: {cube.shape}\n"
            f"File: {image_path}"
        )

    # --------------------------------------------------------
    # Locate spectral dimension
    # --------------------------------------------------------

    spectral_axes = [
        index
        for index, size
        in enumerate(cube.shape)
        if size == EXPECTED_SPECTRAL_BANDS
    ]

    if not spectral_axes:

        raise ValueError(
            f"\nCould not identify the "
            f"{EXPECTED_SPECTRAL_BANDS}-band spectral axis.\n"
            f"Image shape: {cube.shape}\n"
            f"File: {image_path}"
        )

    spectral_axis = spectral_axes[0]

    # --------------------------------------------------------
    # Move spectral axis to last dimension
    # --------------------------------------------------------

    cube = np.moveaxis(
        cube,
        spectral_axis,
        -1
    )

    cube = cube.astype(
        np.float32
    )

    return cube


# ============================================================
# EXTRACT SPECTRAL SIGNATURE
# ============================================================

def extract_spectral_signature(
    cube
):

    """
    Convert the hyperspectral leaf cube into
    one 204-dimensional spectral signature.

    Background pixels are ignored.
    """

    cube = np.asarray(
        cube,
        dtype=np.float32
    )

    height, width, bands = cube.shape

    if bands != EXPECTED_SPECTRAL_BANDS:

        raise ValueError(
            f"\nExpected "
            f"{EXPECTED_SPECTRAL_BANDS} bands.\n"
            f"Received: {bands}"
        )

    # --------------------------------------------------------
    # Calculate pixel energy
    # --------------------------------------------------------

    pixel_energy = np.sum(
        np.abs(cube),
        axis=2
    )

    # --------------------------------------------------------
    # Remove background
    # --------------------------------------------------------

    mask = (
        pixel_energy > 0
    )

    if not np.any(mask):

        raise ValueError(
            "No valid leaf pixels found."
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
# LOAD TRAINING CSV
# ============================================================

def load_metadata():

    if not os.path.exists(
        TRAIN_CSV
    ):

        raise FileNotFoundError(
            f"\ntrain.csv not found:\n"
            f"{TRAIN_CSV}"
        )

    df = pd.read_csv(
        TRAIN_CSV
    )

    required_columns = [
        "ImageId"
    ] + TARGET_COLUMNS

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "\nMissing columns:\n"
            + "\n".join(
                missing_columns
            )
        )

    return df


# ============================================================
# BUILD DATASET
# ============================================================

def build_dataset(
    max_samples=None,
    verbose=True
):

    df = load_metadata()

    if max_samples is not None:

        df = df.head(
            int(max_samples)
        )

    features = []
    targets = []

    total = len(
        df
    )

    if verbose:

        print(
            "\n========================================"
        )

        print(
            "       HYPERLEAF DATASET BUILDER"
        )

        print(
            "========================================"
        )

        print(
            f"\nDataset: HyperLeaf2024"
        )

        print(
            f"Samples: {total}"
        )

        print(
            f"Spectral bands: "
            f"{EXPECTED_SPECTRAL_BANDS}"
        )

        print(
            "Targets:"
        )

        for target in TARGET_COLUMNS:

            print(
                f"  - {target}"
            )

    # --------------------------------------------------------
    # PROCESS IMAGES
    # --------------------------------------------------------

    for position, (
        index,
        row
    ) in enumerate(
        df.iterrows(),
        start=1
    ):

        image_id = row[
            "ImageId"
        ]

        if verbose:

            print(
                f"\nProcessing "
                f"{position}/{total}"
                f"  ImageId={image_id}"
            )

        try:

            # -----------------------------------------------
            # Find image
            # -----------------------------------------------

            image_path = find_image(
                image_id
            )

            if verbose:

                print(
                    f"  File: "
                    f"{os.path.basename(image_path)}"
                )

            # -----------------------------------------------
            # Load hyperspectral cube
            # -----------------------------------------------

            cube = load_hyperspectral_image(
                image_path
            )

            if verbose:

                print(
                    f"  Cube shape: "
                    f"{cube.shape}"
                )

            # -----------------------------------------------
            # Extract spectral signature
            # -----------------------------------------------

            signature = extract_spectral_signature(
                cube
            )

            # -----------------------------------------------
            # Targets
            # -----------------------------------------------

            target_values = (
                row[
                    TARGET_COLUMNS
                ]
                .astype(float)
                .to_numpy(
                    dtype=np.float32
                )
            )

            if not np.all(
                np.isfinite(
                    target_values
                )
            ):

                print(
                    "  Skipping: invalid targets."
                )

                continue

            features.append(
                signature
            )

            targets.append(
                target_values
            )

            if verbose:

                print(
                    "  Successfully processed."
                )

        except Exception as error:

            print(
                "\n  WARNING:"
            )

            print(
                f"  {error}"
            )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if len(features) == 0:

        raise RuntimeError(
            "\nNo valid samples were created.\n"
            "Check your HyperLeaf image directory."
        )

    X = np.asarray(
        features,
        dtype=np.float32
    )

    y = np.asarray(
        targets,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # Final output
    # --------------------------------------------------------

    if verbose:

        print(
            "\n========================================"
        )

        print(
            "             DATASET READY"
        )

        print(
            "========================================"
        )

        print(
            f"\nFeature shape : {X.shape}"
        )

        print(
            f"Target shape  : {y.shape}"
        )

        print(
            f"Samples       : {len(X)}"
        )

        print(
            f"Spectral bands: {X.shape[1]}"
        )

        print(
            "\nTarget statistics:"
        )

        for i, target in enumerate(
            TARGET_COLUMNS
        ):

            print(
                f"\n{target}"
            )

            print(
                f"  Min  : {y[:, i].min():.6f}"
            )

            print(
                f"  Max  : {y[:, i].max():.6f}"
            )

            print(
                f"  Mean : {y[:, i].mean():.6f}"
            )

            print(
                f"  Std  : {y[:, i].std():.6f}"
            )

        print(
            "\n========================================"
        )

    return X, y


# ============================================================
# SAVE CACHE
# ============================================================

def save_dataset_cache(
    X,
    y
):

    cache_dir = os.path.join(
        BASE_DIR,
        "data",
        "spectral",
        "cache"
    )

    os.makedirs(
        cache_dir,
        exist_ok=True
    )

    cache_path = os.path.join(
        cache_dir,
        "hyperleaf_features.npz"
    )

    np.savez_compressed(
        cache_path,
        X=X,
        y=y
    )

    print(
        "\nDataset cache saved:"
    )

    print(
        cache_path
    )

    return cache_path


# ============================================================
# LOAD CACHE
# ============================================================

def load_cached_dataset():

    cache_path = os.path.join(
        BASE_DIR,
        "data",
        "spectral",
        "cache",
        "hyperleaf_features.npz"
    )

    if not os.path.exists(
        cache_path
    ):

        return None, None

    data = np.load(
        cache_path
    )

    X = data[
        "X"
    ]

    y = data[
        "y"
    ]

    print(
        "\nLoaded cached dataset."
    )

    print(
        f"Features: {X.shape}"
    )

    print(
        f"Targets : {y.shape}"
    )

    return X, y


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\nTesting HyperLeaf dataset loader..."
    )

    # --------------------------------------------------------
    # ONLY ONE IMAGE FOR INITIAL TEST
    # --------------------------------------------------------

    X, y = build_dataset(
        max_samples=1,
        verbose=True
    )

    print(
        "\n========================================"
    )

    print(
        "           FIRST SAMPLE"
    )

    print(
        "========================================"
    )

    print(
        f"\nSpectral vector shape: "
        f"{X[0].shape}"
    )

    print(
        f"Number of bands: "
        f"{len(X[0])}"
    )

    print(
        "\nFirst 10 spectral values:"
    )

    print(
        X[0][:10]
    )

    print(
        "\nTargets:"
    )

    for index, target in enumerate(
        TARGET_COLUMNS
    ):

        print(
            f"{target}: "
            f"{y[0][index]:.6f}"
        )

    print(
        "\n========================================"
    )

    print(
        "DATASET TEST SUCCESSFUL"
    )

    print(
        "========================================"
    )