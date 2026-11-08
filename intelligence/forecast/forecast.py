def generate_forecast(
    current_yield,
    yield_category,
    disease_risk,
    health_score,
    forecast_days=14,
    historical_yields=None,
    historical_risks=None,
    spectral_stress=0.0
):

    current_yield = float(
        current_yield
    )

    disease_risk = float(
        disease_risk
    )

    health_score = float(
        health_score
    )

    forecast_days = int(
        forecast_days
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


    if historical_yields:

        historical_yields = [
            float(value)
            for value in historical_yields
        ]

        average_yield = sum(
            historical_yields
        ) / len(
            historical_yields
        )

        yield_trend = (
            current_yield - average_yield
        )

    else:

        average_yield = current_yield

        yield_trend = 0.0


    if historical_risks:

        historical_risks = [
            float(value)
            for value in historical_risks
        ]

        average_risk = sum(
            historical_risks
        ) / len(
            historical_risks
        )

        risk_trend = (
            disease_risk - average_risk
        )

    else:

        average_risk = disease_risk

        risk_trend = 0.0


    projected_yield = current_yield


    if yield_trend < -1:

        projected_yield *= 0.95

    elif yield_trend > 1:

        projected_yield *= 1.03


    health_factor = (
        100.0 - health_score
    )


    if health_factor >= 60:

        projected_yield *= 0.92

    elif health_factor >= 40:

        projected_yield *= 0.96

    elif health_factor >= 20:

        projected_yield *= 0.98


    if spectral_stress >= 80:

        projected_yield *= 0.94

    elif spectral_stress >= 60:

        projected_yield *= 0.97

    elif spectral_stress >= 40:

        projected_yield *= 0.985


    projected_yield = max(
        0.0,
        projected_yield
    )


    projected_risk = disease_risk


    if risk_trend > 10:

        projected_risk += 10

    elif risk_trend < -10:

        projected_risk -= 10


    spectral_risk_contribution = (
        spectral_stress * 0.15
    )

    projected_risk += (
        spectral_risk_contribution
    )


    if health_score < 40:

        projected_risk += 10

    elif health_score < 60:

        projected_risk += 5


    projected_risk = max(
        0.0,
        min(
            100.0,
            projected_risk
        )
    )


    if projected_risk >= 75:

        future_risk = "Critical"

    elif projected_risk >= 55:

        future_risk = "High"

    elif projected_risk >= 35:

        future_risk = "Moderate"

    elif projected_risk >= 15:

        future_risk = "Low"

    else:

        future_risk = "Minimal"


    if (
        not historical_yields
        and not historical_risks
    ):

        forecast_type = "baseline"

    else:

        forecast_type = "historical_trend"


    if spectral_stress >= 70:

        forecast_signal = (
            "Strong stress signal detected"
        )

    elif spectral_stress >= 40:

        forecast_signal = (
            "Moderate stress signal detected"
        )

    elif spectral_stress >= 20:

        forecast_signal = (
            "Early stress signal detected"
        )

    else:

        forecast_signal = (
            "No significant spectral stress"
        )


    return {

        "forecast_days": forecast_days,

        "current_yield": round(
            current_yield,
            3
        ),

        "projected_yield": round(
            projected_yield,
            3
        ),

        "current_disease_risk": round(
            disease_risk,
            2
        ),

        "projected_disease_risk": round(
            projected_risk,
            2
        ),

        "future_risk_level": future_risk,

        "yield_trend": round(
            yield_trend,
            3
        ),

        "risk_trend": round(
            risk_trend,
            3
        ),

        "spectral_stress": round(
            spectral_stress,
            2
        ),

        "spectral_risk_contribution": round(
            spectral_risk_contribution,
            2
        ),

        "forecast_signal": forecast_signal,

        "health_score": round(
            health_score,
            2
        ),

        "forecast_type": forecast_type
    }