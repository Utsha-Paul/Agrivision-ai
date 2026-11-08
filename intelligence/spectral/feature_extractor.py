import cv2
import numpy as np


def masked_pixels(
    image,
    mask
):

    pixels = image[
        mask > 0
    ]

    if len(pixels) == 0:

        pixels = image.reshape(
            -1,
            image.shape[-1]
        )

    return pixels


def safe_mean(
    values
):

    if len(values) == 0:
        return 0.0

    return float(
        np.mean(values)
    )


def safe_std(
    values
):

    if len(values) == 0:
        return 0.0

    return float(
        np.std(values)
    )


def calculate_rgb_features(
    image,
    mask
):

    pixels = masked_pixels(
        image,
        mask
    )

    red = pixels[:, 0].astype(
        np.float32
    )

    green = pixels[:, 1].astype(
        np.float32
    )

    blue = pixels[:, 2].astype(
        np.float32
    )


    total = (
        red
        +
        green
        +
        blue
        +
        1e-6
    )


    normalized_red = (
        red / total
    )

    normalized_green = (
        green / total
    )

    normalized_blue = (
        blue / total
    )


    return {

        "red_mean": safe_mean(
            red
        ),

        "green_mean": safe_mean(
            green
        ),

        "blue_mean": safe_mean(
            blue
        ),

        "red_std": safe_std(
            red
        ),

        "green_std": safe_std(
            green
        ),

        "blue_std": safe_std(
            blue
        ),

        "normalized_red_mean":
            safe_mean(
                normalized_red
            ),

        "normalized_green_mean":
            safe_mean(
                normalized_green
            ),

        "normalized_blue_mean":
            safe_mean(
                normalized_blue
            )
    }


def calculate_hsv_features(
    image,
    mask
):

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2HSV
    )

    pixels = masked_pixels(
        hsv,
        mask
    )

    hue = pixels[:, 0].astype(
        np.float32
    )

    saturation = pixels[:, 1].astype(
        np.float32
    )

    value = pixels[:, 2].astype(
        np.float32
    )


    return {

        "hue_mean": safe_mean(
            hue
        ),

        "hue_std": safe_std(
            hue
        ),

        "saturation_mean":
            safe_mean(
                saturation
            ),

        "saturation_std":
            safe_std(
                saturation
            ),

        "brightness_mean":
            safe_mean(
                value
            ),

        "brightness_std":
            safe_std(
                value
            )
    }


def calculate_vegetation_indices(
    image,
    mask
):

    pixels = masked_pixels(
        image,
        mask
    ).astype(
        np.float32
    )


    red = pixels[:, 0]
    green = pixels[:, 1]
    blue = pixels[:, 2]


    exg = (
        2.0 * green
        -
        red
        -
        blue
    )


    green_red_ratio = (
        green
        /
        (red + 1.0)
    )


    ngrdi = (
        (green - red)
        /
        (green + red + 1.0)
    )


    rgb_vi = (
        green
        /
        (
            red
            +
            green
            +
            blue
            +
            1.0
        )
    )


    return {

        "excess_green_index":
            safe_mean(
                exg
            ),

        "green_red_ratio":
            safe_mean(
                green_red_ratio
            ),

        "ngrdi":
            safe_mean(
                ngrdi
            ),

        "rgb_vegetation_index":
            safe_mean(
                rgb_vi
            )
    }


def calculate_stress_features(
    image,
    mask
):

    pixels = masked_pixels(
        image,
        mask
    ).astype(
        np.float32
    )


    red = pixels[:, 0]
    green = pixels[:, 1]
    blue = pixels[:, 2]


    total = (
        red
        +
        green
        +
        blue
        +
        1.0
    )


    green_ratio = (
        green / total
    )

    red_ratio = (
        red / total
    )


    stress_ratio = (
        red_ratio
        /
        (
            green_ratio
            +
            1e-6
        )
    )


    yellow_pixels = (
        (red > green * 0.85)
        &
        (green > blue * 1.10)
    )


    brown_pixels = (
        (red > green * 1.15)
        &
        (green > blue * 1.10)
    )


    yellow_ratio = (
        np.mean(
            yellow_pixels
        )
    )


    brown_ratio = (
        np.mean(
            brown_pixels
        )
    )


    return {

        "red_green_stress_ratio":
            safe_mean(
                stress_ratio
            ),

        "yellow_pixel_ratio":
            float(
                yellow_ratio
            ),

        "brown_pixel_ratio":
            float(
                brown_ratio
            )
    }


def extract_spectral_features(
    processed_data
):

    image = processed_data[
        "image"
    ]

    mask = processed_data[
        "mask"
    ]


    features = {}

    features.update(
        calculate_rgb_features(
            image,
            mask
        )
    )

    features.update(
        calculate_hsv_features(
            image,
            mask
        )
    )

    features.update(
        calculate_vegetation_indices(
            image,
            mask
        )
    )

    features.update(
        calculate_stress_features(
            image,
            mask
        )
    )


    features[
        "leaf_area_ratio"
    ] = float(
        np.mean(
            mask > 0
        )
    )


    return features