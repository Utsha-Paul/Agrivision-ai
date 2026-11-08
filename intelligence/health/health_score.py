def calculate_health_score(
    yield_value,
    yield_category,
    disease,
    disease_confidence,
    crop_consistency=True,
    pest_index=0,
    humidity_pct=0,
    soil_ph=7.0,
    spectral_stress=0.0
):

    score = 100.0

    disease_name = str(
        disease
    ).lower().strip()

    confidence = float(
        disease_confidence
    )

    yield_category = str(
        yield_category
    ).lower().strip()

    if (
        "healthy" not in disease_name
        and "no disease" not in disease_name
    ):
        if confidence >= 90:
            score -= 40

        elif confidence >= 75:
            score -= 32

        elif confidence >= 60:
            score -= 24

        elif confidence >= 40:
            score -= 15

        else:
            score -= 8

    yield_penalties = {
        "low": 30,
        "moderate": 18,
        "good": 7,
        "high": 0
    }

    score -= yield_penalties.get(
        yield_category,
        10
    )

    pest_index = float(
        pest_index
    )

    if pest_index >= 75:
        score -= 15

    elif pest_index >= 50:
        score -= 10

    elif pest_index >= 25:
        score -= 5

    humidity_pct = float(
        humidity_pct
    )

    if humidity_pct >= 90:
        score -= 5

    elif humidity_pct >= 80:
        score -= 3

    soil_ph = float(
        soil_ph
    )

    if soil_ph < 5.0 or soil_ph > 8.5:
        score -= 8

    elif soil_ph < 5.5 or soil_ph > 8.0:
        score -= 4

    if not crop_consistency:
        score -= 10

    spectral_stress = float(
        spectral_stress
    )

    spectral_stress = max(
        0.0,
        min(
            100.0,
            spectral_stress
        )
    )

    if spectral_stress >= 80:
        spectral_penalty = 20

    elif spectral_stress >= 60:
        spectral_penalty = 15

    elif spectral_stress >= 40:
        spectral_penalty = 10

    elif spectral_stress >= 20:
        spectral_penalty = 5

    else:
        spectral_penalty = 0

    score -= spectral_penalty

    score = max(
        0.0,
        min(
            100.0,
            score
        )
    )

    if score >= 90:
        status = "Excellent"

    elif score >= 75:
        status = "Healthy"

    elif score >= 60:
        status = "Moderate"

    elif score >= 40:
        status = "At Risk"

    else:
        status = "Poor"

    return {
        "health_score": round(
            score,
            2
        ),
        "health_status": status,
        "spectral_stress": round(
            spectral_stress,
            2
        ),
        "spectral_penalty": round(
            spectral_penalty,
            2
        )
    }