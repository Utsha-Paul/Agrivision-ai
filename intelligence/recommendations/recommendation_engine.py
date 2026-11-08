def generate_recommendations(
    crop,
    disease,
    disease_confidence,
    yield_category,
    health_score,
    health_status,
    risk_level,
    pest_index=0,
    humidity_pct=0,
    soil_ph=7.0,
    spectral_stress=0.0
):

    recommendations = []
    priorities = []

    crop = str(
        crop
    )

    disease = str(
        disease
    )

    disease_confidence = float(
        disease_confidence
    )

    health_score = float(
        health_score
    )

    pest_index = float(
        pest_index
    )

    humidity_pct = float(
        humidity_pct
    )

    soil_ph = float(
        soil_ph
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

    disease_lower = disease.lower()


    # ----------------------------------------
    # DISEASE MANAGEMENT
    # ----------------------------------------

    if (
        "healthy" not in disease_lower
        and "no disease" not in disease_lower
    ):

        priorities.append(
            "Disease management"
        )

        if disease_confidence >= 90:

            recommendations.append(
                "High-confidence disease detection. "
                "Inspect affected plants and consider "
                "appropriate disease-management practices."
            )

        elif disease_confidence >= 60:

            recommendations.append(
                "Disease detected with moderate-to-high "
                "confidence. Inspect additional leaves "
                "before taking corrective action."
            )

        else:

            recommendations.append(
                "Disease prediction has lower confidence. "
                "Capture additional clear leaf images "
                "for confirmation."
            )

    else:

        recommendations.append(
            "No major disease was detected in the "
            "uploaded leaf image."
        )


    # ----------------------------------------
    # YIELD MANAGEMENT
    # ----------------------------------------

    yield_lower = yield_category.lower()

    if yield_lower == "low":

        priorities.append(
            "Yield improvement"
        )

        recommendations.append(
            "Predicted yield is low. Review soil nutrients, "
            "irrigation, weather conditions and pest pressure."
        )

    elif yield_lower == "moderate":

        priorities.append(
            "Yield optimization"
        )

        recommendations.append(
            "Predicted yield is moderate. Review farm inputs "
            "and optimize irrigation and nutrient management."
        )

    elif yield_lower == "good":

        recommendations.append(
            "Predicted yield is good. Continue monitoring "
            "crop conditions and maintain current practices."
        )

    else:

        recommendations.append(
            "Predicted yield is high. Maintain current "
            "farm-management practices and monitor crop health."
        )


    # ----------------------------------------
    # PEST MANAGEMENT
    # ----------------------------------------

    if pest_index >= 75:

        priorities.append(
            "Pest management"
        )

        recommendations.append(
            "Pest index is high. Inspect the field regularly "
            "for pest activity and use appropriate integrated "
            "pest-management practices."
        )

    elif pest_index >= 50:

        recommendations.append(
            "Moderate pest pressure detected. Increase field "
            "monitoring."
        )


    # ----------------------------------------
    # ENVIRONMENTAL MANAGEMENT
    # ----------------------------------------

    if humidity_pct >= 85:

        priorities.append(
            "Environmental monitoring"
        )

        recommendations.append(
            "High humidity may increase the risk of some "
            "plant diseases. Increase monitoring of leaves "
            "and canopy conditions."
        )


    # ----------------------------------------
    # SOIL MANAGEMENT
    # ----------------------------------------

    if soil_ph < 5.5:

        priorities.append(
            "Soil management"
        )

        recommendations.append(
            "Soil pH is relatively acidic. Consider soil "
            "testing and appropriate soil-management practices."
        )

    elif soil_ph > 8.0:

        priorities.append(
            "Soil management"
        )

        recommendations.append(
            "Soil pH is relatively alkaline. Consider soil "
            "testing and appropriate soil-management practices."
        )


    # ----------------------------------------
    # SPECTRAL STRESS ANALYSIS
    # ----------------------------------------

    if spectral_stress >= 80:

        priorities.append(
            "Severe spectral stress"
        )

        recommendations.insert(
            0,
            "Strong spectral stress detected. "
            "Prioritize field inspection and investigate "
            "possible disease, nutrient, water or environmental stress."
        )

    elif spectral_stress >= 60:

        priorities.append(
            "High spectral stress"
        )

        recommendations.append(
            "High spectral stress detected. Inspect the crop "
            "for early signs of disease, nutrient deficiency, "
            "water stress or environmental stress."
        )

    elif spectral_stress >= 40:

        priorities.append(
            "Spectral stress monitoring"
        )

        recommendations.append(
            "Moderate spectral stress detected. Increase "
            "crop monitoring and compare future images "
            "to identify changes in plant condition."
        )

    elif spectral_stress >= 20:

        priorities.append(
            "Early stress monitoring"
        )

        recommendations.append(
            "Early spectral stress signal detected. "
            "Continue monitoring the crop and review "
            "irrigation, nutrients and environmental conditions."
        )

    else:

        recommendations.append(
            "No significant spectral stress detected "
            "in the analyzed image."
        )


    # ----------------------------------------
    # HEALTH SCORE
    # ----------------------------------------

    if health_score < 40:

        priorities.append(
            "Immediate crop monitoring"
        )

        recommendations.append(
            "Overall crop health is poor. Increase monitoring "
            "frequency and investigate the main contributing factors."
        )

    elif health_score < 60:

        priorities.append(
            "Crop monitoring"
        )

        recommendations.append(
            "Crop health is at risk. Closely monitor disease, "
            "pests, soil and environmental conditions."
        )

    elif health_score < 75:

        recommendations.append(
            "Crop health is moderate. Continue monitoring "
            "and optimize farm inputs where necessary."
        )

    else:

        recommendations.append(
            "Overall crop health is currently favorable. "
            "Continue regular monitoring."
        )


    # ----------------------------------------
    # RISK LEVEL
    # ----------------------------------------

    risk_lower = str(
        risk_level
    ).lower()


    if risk_lower == "critical":

        recommendations.insert(
            0,
            "Critical risk detected. Prioritize field inspection "
            "and verify the AI results before taking action."
        )

    elif risk_lower == "high":

        recommendations.insert(
            0,
            "High crop risk detected. Increase monitoring "
            "and investigate the identified risk factors."
        )


    # ----------------------------------------
    # COMBINATION ALERTS
    # ----------------------------------------

    if (
        spectral_stress >= 60
        and
        "healthy" not in disease_lower
        and
        "no disease" not in disease_lower
        and
        disease_confidence >= 60
    ):

        priorities.append(
            "Disease + spectral confirmation"
        )

        recommendations.insert(
            0,
            "Disease detection and spectral stress signals "
            "both indicate crop stress. Prioritize inspection "
            "of affected plants and surrounding crop areas."
        )


    if (
        spectral_stress >= 60
        and
        health_score < 60
    ):

        priorities.append(
            "High-priority crop assessment"
        )

        recommendations.insert(
            0,
            "Multiple indicators show crop stress. "
            "Perform a detailed field assessment and "
            "review irrigation, nutrition, pests and disease."
        )


    # ----------------------------------------
    # REMOVE DUPLICATES
    # ----------------------------------------

    unique_recommendations = []

    for recommendation in recommendations:

        if recommendation not in unique_recommendations:

            unique_recommendations.append(
                recommendation
            )


    unique_priorities = list(
        dict.fromkeys(
            priorities
        )
    )


    # ----------------------------------------
    # RETURN RESULTS
    # ----------------------------------------

    return {

        "crop": crop,

        "priority_areas": unique_priorities,

        "recommendations": unique_recommendations,

        "recommendation_count": len(
            unique_recommendations
        ),

        "spectral_stress": round(
            spectral_stress,
            2
        )
    }