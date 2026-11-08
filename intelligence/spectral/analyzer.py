def classify_stress(
    stress_score
):

    if stress_score >= 75:
        return "Severe"

    if stress_score >= 50:
        return "High"

    if stress_score >= 25:
        return "Moderate"

    return "Low"


def analyze_spectral_features(
    features
):

    ngrdi = float(
        features.get(
            "ngrdi",
            0
        )
    )

    exg = float(
        features.get(
            "excess_green_index",
            0
        )
    )

    yellow_ratio = float(
        features.get(
            "yellow_pixel_ratio",
            0
        )
    )

    brown_ratio = float(
        features.get(
            "brown_pixel_ratio",
            0
        )
    )

    saturation = float(
        features.get(
            "saturation_mean",
            0
        )
    )

    green_ratio = float(
        features.get(
            "normalized_green_mean",
            0
        )
    )


    stress_score = 0.0


    if ngrdi < -0.10:

        stress_score += 30

    elif ngrdi < 0:

        stress_score += 20

    elif ngrdi < 0.10:

        stress_score += 10


    if exg < 20:

        stress_score += 20

    elif exg < 40:

        stress_score += 10


    if yellow_ratio > 0.30:

        stress_score += 20

    elif yellow_ratio > 0.15:

        stress_score += 10


    if brown_ratio > 0.20:

        stress_score += 20

    elif brown_ratio > 0.10:

        stress_score += 10


    if saturation < 60:

        stress_score += 10


    if green_ratio < 0.25:

        stress_score += 10


    stress_score = max(
        0.0,
        min(
            100.0,
            stress_score
        )
    )


    stress_level = classify_stress(
        stress_score
    )


    if ngrdi >= 0.10:

        vegetation_condition = "Healthy"

    elif ngrdi >= 0:

        vegetation_condition = "Moderate"

    else:

        vegetation_condition = "Reduced"


    if yellow_ratio > 0.20:

        discoloration = "High"

    elif yellow_ratio > 0.10:

        discoloration = "Moderate"

    else:

        discoloration = "Low"


    if brown_ratio > 0.15:

        tissue_damage = "High"

    elif brown_ratio > 0.07:

        tissue_damage = "Moderate"

    else:

        tissue_damage = "Low"


    return {

        "spectral_stress_score":
            round(
                stress_score,
                2
            ),

        "stress_level":
            stress_level,

        "vegetation_condition":
            vegetation_condition,

        "discoloration_level":
            discoloration,

        "tissue_damage_level":
            tissue_damage,

        "vegetation_index":
            round(
                ngrdi,
                4
            ),

        "excess_green_index":
            round(
                exg,
                2
            ),

        "green_ratio":
            round(
                green_ratio,
                4
            ),

        "saturation":
            round(
                saturation,
                2
            )
    }


def analyze_leaf_spectrum(
    processed_data
):

    from .feature_extractor import (
        extract_spectral_features
    )

    features = extract_spectral_features(
        processed_data
    )

    analysis = analyze_spectral_features(
        features
    )

    return {
        "features": features,
        "analysis": analysis
    }