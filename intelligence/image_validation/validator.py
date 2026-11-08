import os

import cv2
import numpy as np


def validate_crop_image(
    image_path
):

    result = {
        "valid": False,
        "status": "Invalid",
        "reason": "",
        "vegetation_ratio": 0.0,
        "green_ratio": 0.0,
        "brightness": 0.0
    }

    if not image_path:

        result["reason"] = (
            "No image was selected."
        )

        return result


    if not os.path.exists(
        image_path
    ):

        result["reason"] = (
            "Image file does not exist."
        )

        return result


    image = cv2.imread(
        image_path
    )

    if image is None:

        result["reason"] = (
            "Unable to read the image."
        )

        return result


    height, width = image.shape[:2]


    if height < 100 or width < 100:

        result["reason"] = (
            "Image resolution is too low."
        )

        return result


    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )


    # ----------------------------------------
    # GREEN VEGETATION DETECTION
    # ----------------------------------------

    lower_green = np.array(
        [20, 30, 20],
        dtype=np.uint8
    )

    upper_green = np.array(
        [100, 255, 255],
        dtype=np.uint8
    )

    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )


    green_pixels = np.sum(
        green_mask > 0
    )

    total_pixels = (
        image.shape[0]
        *
        image.shape[1]
    )

    green_ratio = (
        green_pixels
        /
        max(
            total_pixels,
            1
        )
    )


    # ----------------------------------------
    # GENERAL VEGETATION DETECTION
    # ----------------------------------------

    saturation = hsv[:, :, 1]

    value = hsv[:, :, 2]


    vegetation_mask = (
        (saturation > 25)
        &
        (value > 30)
    )


    vegetation_pixels = np.sum(
        vegetation_mask
    )


    vegetation_ratio = (
        vegetation_pixels
        /
        max(
            total_pixels,
            1
        )
    )


    # ----------------------------------------
    # BRIGHTNESS
    # ----------------------------------------

    brightness = float(
        np.mean(value)
    )


    result[
        "vegetation_ratio"
    ] = round(
        float(
            vegetation_ratio
        ),
        4
    )

    result[
        "green_ratio"
    ] = round(
        float(
            green_ratio
        ),
        4
    )

    result[
        "brightness"
    ] = round(
        brightness,
        2
    )


    # ----------------------------------------
    # IMAGE QUALITY
    # ----------------------------------------

    if brightness < 15:

        result["reason"] = (
            "Image is too dark."
        )

        return result


    if brightness > 250:

        result["reason"] = (
            "Image is severely overexposed."
        )

        return result


    # ----------------------------------------
    # VEGETATION DECISION
    # ----------------------------------------

    if (
        green_ratio >= 0.08
        or vegetation_ratio >= 0.25
    ):

        result["valid"] = True

        result["status"] = (
            "Crop image detected"
        )

        result["reason"] = (
            "Image contains sufficient "
            "vegetation-like regions."
        )

        return result


    # ----------------------------------------
    # FALLBACK FOR DISEASED LEAVES
    # ----------------------------------------
    #
    # A severely diseased leaf may not
    # contain much green.
    #

    if vegetation_ratio >= 0.12:

        result["valid"] = True

        result["status"] = (
            "Possible crop image"
        )

        result["reason"] = (
            "Image contains vegetation-like "
            "regions but limited green coloration."
        )

        return result


    result["reason"] = (
        "No sufficient leaf or vegetation "
        "region detected."
    )

    return result