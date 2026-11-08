def calculate_risk(
    disease,
    disease_confidence,
    yield_category,
    pest_index=0,
    humidity_pct=0,
    crop_consistency=True,
    spectral_stress=0.0
):

    disease_name = str(
        disease
    ).lower().strip()

    confidence = float(
        disease_confidence
    )

    pest_index = float(
        pest_index
    )

    humidity_pct = float(
        humidity_pct
    )

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

    disease_risk = 0

    if (
        "healthy" in disease_name
        or "no disease" in disease_name
    ):
        disease_risk = 0

    elif confidence >= 90:
        disease_risk = 80

    elif confidence >= 75:
        disease_risk = 65

    elif confidence >= 60:
        disease_risk = 50

    elif confidence >= 40:
        disease_risk = 35

    else:
        disease_risk = 20


    pest_risk = min(
        100,
        pest_index
    )


    environmental_risk = 0

    if humidity_pct >= 90:
        environmental_risk = 80

    elif humidity_pct >= 80:
        environmental_risk = 65

    elif humidity_pct >= 70:
        environmental_risk = 45

    elif humidity_pct >= 50:
        environmental_risk = 25

    else:
        environmental_risk = 15


    yield_risk_map = {
        "low": 80,
        "moderate": 55,
        "good": 25,
        "high": 10
    }

    yield_risk = yield_risk_map.get(
        str(
            yield_category
        ).lower().strip(),
        50
    )


    if crop_consistency:
        consistency_risk = 0

    else:
        consistency_risk = 60


    spectral_risk = spectral_stress


    overall_risk = (
        disease_risk * 0.35
        +
        pest_risk * 0.15
        +
        environmental_risk * 0.15
        +
        yield_risk * 0.15
        +
        consistency_risk * 0.05
        +
        spectral_risk * 0.15
    )


    overall_risk = max(
        0,
        min(
            100,
            overall_risk
        )
    )


    if overall_risk >= 75:
        risk_level = "Critical"

    elif overall_risk >= 55:
        risk_level = "High"

    elif overall_risk >= 35:
        risk_level = "Moderate"

    elif overall_risk >= 15:
        risk_level = "Low"

    else:
        risk_level = "Minimal"


    return {
        "overall_risk_score": round(
            overall_risk,
            2
        ),

        "risk_level": risk_level,

        "disease_risk": round(
            disease_risk,
            2
        ),

        "pest_risk": round(
            pest_risk,
            2
        ),

        "environmental_risk": round(
            environmental_risk,
            2
        ),

        "yield_risk": round(
            yield_risk,
            2
        ),

        "consistency_risk": round(
            consistency_risk,
            2
        ),

        "spectral_risk": round(
            spectral_risk,
            2
        )
    }