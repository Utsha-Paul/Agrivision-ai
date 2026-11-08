import os
import cv2
import numpy as np


IMAGE_SIZE = (224, 224)


def load_image(image_path):

    if not image_path:
        raise ValueError(
            "Image path cannot be empty."
        )

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )

    image = cv2.imread(
        image_path
    )

    if image is None:
        raise ValueError(
            "Unable to read image."
        )

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    return image


def resize_image(image):

    return cv2.resize(
        image,
        IMAGE_SIZE,
        interpolation=cv2.INTER_AREA
    )


def normalize_image(image):

    image = image.astype(
        np.float32
    ) / 255.0

    return image


def create_leaf_mask(image):

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2HSV
    )

    lower_green = np.array(
        [20, 25, 20],
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

    saturation = hsv[:, :, 1]

    saturation_mask = np.where(
        saturation > 25,
        255,
        0
    ).astype(
        np.uint8
    )

    mask = cv2.bitwise_or(
        green_mask,
        saturation_mask
    )

    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    return mask


def preprocess_leaf_image(
    image_path
):

    image = load_image(
        image_path
    )

    resized = resize_image(
        image
    )

    normalized = normalize_image(
        resized
    )

    mask = create_leaf_mask(
        resized
    )

    return {
        "original": image,
        "image": resized,
        "normalized": normalized,
        "mask": mask
    }