import os

import cv2
import numpy as np


def generate_stress_visualization(
    image_path,
    output_dir="outputs/spectral"
):

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

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    original = image.copy()

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    rgb_float = (
        rgb.astype(
            np.float32
        ) / 255.0
    )

    r = rgb_float[:, :, 0]
    g = rgb_float[:, :, 1]
    b = rgb_float[:, :, 2]

    # ----------------------------------------
    # EXCESS GREEN INDEX
    # ----------------------------------------

    exg = (
        2.0 * g
        - r
        - b
    )

    exg_min = np.percentile(
        exg,
        2
    )

    exg_max = np.percentile(
        exg,
        98
    )

    exg_norm = (
        exg - exg_min
    ) / (
        exg_max - exg_min + 1e-8
    )

    exg_norm = np.clip(
        exg_norm,
        0,
        1
    )

    # ----------------------------------------
    # NORMALIZED GREEN INDEX
    # ----------------------------------------

    ndi = (
        g - r
    ) / (
        g + r + 1e-8
    )

    ndi_min = np.percentile(
        ndi,
        2
    )

    ndi_max = np.percentile(
        ndi,
        98
    )

    ndi_norm = (
        ndi - ndi_min
    ) / (
        ndi_max - ndi_min + 1e-8
    )

    ndi_norm = np.clip(
        ndi_norm,
        0,
        1
    )

    # ----------------------------------------
    # HSV ANALYSIS
    # ----------------------------------------

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    hue = hsv[:, :, 0].astype(
        np.float32
    )

    saturation = (
        hsv[:, :, 1].astype(
            np.float32
        ) / 255.0
    )

    value = (
        hsv[:, :, 2].astype(
            np.float32
        ) / 255.0
    )

    # ----------------------------------------
    # VEGETATION MASK
    # ----------------------------------------

    green_mask = (
        (hue >= 20)
        &
        (hue <= 100)
        &
        (saturation >= 0.20)
        &
        (value >= 0.15)
    )

    # Include yellow/brown diseased tissue
    vegetation_like = (
        (saturation >= 0.15)
        &
        (value >= 0.12)
        &
        (
            (ndi > -0.35)
            |
            (exg > -0.20)
        )
    )

    vegetation_mask = (
        green_mask
        |
        vegetation_like
    )

    vegetation_mask = (
        vegetation_mask.astype(
            np.uint8
        ) * 255
    )

    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    vegetation_mask = cv2.morphologyEx(
        vegetation_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    vegetation_mask = cv2.morphologyEx(
        vegetation_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ----------------------------------------
    # STRESS SCORE
    # ----------------------------------------

    green_loss = (
        1.0 - exg_norm
    )

    ndi_loss = (
        1.0 - ndi_norm
    )

    yellow_brown_factor = (
        np.clip(
            (r + g - 2 * b) / 2.0,
            0,
            1
        )
    )

    stress = (
        0.50 * green_loss
        +
        0.35 * ndi_loss
        +
        0.15 * yellow_brown_factor
    )

    stress = np.clip(
        stress,
        0,
        1
    )

    # ----------------------------------------
    # REMOVE BACKGROUND
    # ----------------------------------------

    mask_float = (
        vegetation_mask.astype(
            np.float32
        ) / 255.0
    )

    stress = (
        stress
        *
        mask_float
    )

    # ----------------------------------------
    # SMOOTH STRESS MAP
    # ----------------------------------------

    stress_uint8 = (
        stress * 255
    ).astype(
        np.uint8
    )

    stress_uint8 = cv2.GaussianBlur(
        stress_uint8,
        (7, 7),
        0
    )

    # ----------------------------------------
    # HEATMAP
    # ----------------------------------------

    heatmap = cv2.applyColorMap(
        stress_uint8,
        cv2.COLORMAP_JET
    )

    heatmap[
        vegetation_mask == 0
    ] = 0

    # ----------------------------------------
    # OVERLAY
    # ----------------------------------------

    overlay = cv2.addWeighted(
        original,
        0.60,
        heatmap,
        0.40,
        0
    )

    overlay[
        vegetation_mask == 0
    ] = original[
        vegetation_mask == 0
    ]

    # ----------------------------------------
    # STRESS THRESHOLD
    # ----------------------------------------

    stress_threshold = 0.55

    stress_region = (
        (
            stress
            >=
            stress_threshold
        )
        &
        (
            vegetation_mask > 0
        )
    )

    stress_region_uint8 = (
        stress_region.astype(
            np.uint8
        ) * 255
    )

    stress_region_uint8 = cv2.morphologyEx(
        stress_region_uint8,
        cv2.MORPH_OPEN,
        kernel
    )

    stress_region_uint8 = cv2.morphologyEx(
        stress_region_uint8,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ----------------------------------------
    # CONTOURS
    # ----------------------------------------

    contours, _ = cv2.findContours(
        stress_region_uint8,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    marked_image = original.copy()

    valid_contours = []

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area < 100:
            continue

        valid_contours.append(
            contour
        )

        cv2.drawContours(
            marked_image,
            [contour],
            -1,
            (0, 0, 255),
            2
        )

    # ----------------------------------------
    # AFFECTED AREA
    # ----------------------------------------

    vegetation_pixels = np.sum(
        vegetation_mask > 0
    )

    stressed_pixels = np.sum(
        stress_region_uint8 > 0
    )

    if vegetation_pixels > 0:

        affected_area_percentage = (
            stressed_pixels
            /
            vegetation_pixels
        ) * 100.0

    else:

        affected_area_percentage = 0.0

    # ----------------------------------------
    # OVERALL STRESS
    # ----------------------------------------

    valid_stress = stress[
        vegetation_mask > 0
    ]

    if len(valid_stress) > 0:

        average_stress = (
            float(
                np.mean(
                    valid_stress
                )
            ) * 100.0
        )

    else:

        average_stress = 0.0

    # ----------------------------------------
    # STRESS LEVEL
    # ----------------------------------------

    if average_stress >= 75:

        stress_level = "Severe"

    elif average_stress >= 55:

        stress_level = "High"

    elif average_stress >= 35:

        stress_level = "Moderate"

    elif average_stress >= 15:

        stress_level = "Low"

    else:

        stress_level = "Healthy"

    # ----------------------------------------
    # SAVE OUTPUTS
    # ----------------------------------------

    base_name = os.path.splitext(
        os.path.basename(
            image_path
        )
    )[0]

    heatmap_path = os.path.join(
        output_dir,
        f"{base_name}_heatmap.jpg"
    )

    overlay_path = os.path.join(
        output_dir,
        f"{base_name}_overlay.jpg"
    )

    marked_path = os.path.join(
        output_dir,
        f"{base_name}_marked.jpg"
    )

    mask_path = os.path.join(
        output_dir,
        f"{base_name}_mask.png"
    )

    cv2.imwrite(
        heatmap_path,
        heatmap
    )

    cv2.imwrite(
        overlay_path,
        overlay
    )

    cv2.imwrite(
        marked_path,
        marked_image
    )

    cv2.imwrite(
        mask_path,
        stress_region_uint8
    )

    return {
        "average_stress": round(
            average_stress,
            2
        ),
        "stress_level": stress_level,
        "affected_area_percentage": round(
            affected_area_percentage,
            2
        ),
        "stressed_pixels": int(
            stressed_pixels
        ),
        "vegetation_pixels": int(
            vegetation_pixels
        ),
        "num_stressed_regions": len(
            valid_contours
        ),
        "heatmap_path": heatmap_path,
        "overlay_path": overlay_path,
        "marked_path": marked_path,
        "mask_path": mask_path
    }