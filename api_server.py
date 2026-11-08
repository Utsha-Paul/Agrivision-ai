import os
import io
import sys
import json
import uuid
import time
import base64
import shutil
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from PIL import Image

# Add current directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import ML and Intelligence pipelines
from module1.disease_detection.predict import predict_disease
from module1.yield_prediction.predict import predict_crop_yield
from intelligence.image_validation.validator import validate_crop_image
from intelligence.health.health_score import calculate_health_score
from intelligence.risk.risk_engine import calculate_risk
from intelligence.forecast.forecast import generate_forecast
from intelligence.recommendations.recommendation_engine import generate_recommendations
from intelligence.spectral.preprocessing import preprocess_leaf_image
from intelligence.spectral.analyzer import analyze_leaf_spectrum
from intelligence.spectral.visualizer import generate_stress_visualization
from intelligence.spectral.model.predict import predict_spectral
from intelligence.forecasting.lstm_trend_engine import run_lstm_trend_analysis
from intelligence.generative.gan_report_engine import generate_gan_report

app = FastAPI(title="AgriVision AI Backend Engine", version="2.5.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and output directories
UPLOAD_DIR = os.path.join(BASE_DIR, "outputs", "web_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
SPECTRAL_OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "spectral")
os.makedirs(SPECTRAL_OUTPUT_DIR, exist_ok=True)
SAMPLES_DIR = os.path.join(BASE_DIR, "outputs", "sample_leaves")
os.makedirs(SAMPLES_DIR, exist_ok=True)

# Mount outputs for image serving
app.mount("/outputs", StaticFiles(directory=os.path.join(BASE_DIR, "outputs")), name="outputs")

FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")

# In-memory session store & registered users
USERS_DB = {
    "rishu@agrivision.ai": {
        "id": "usr-rishu-01",
        "name": "Rishu Kumar Singh",
        "email": "rishu@agrivision.ai",
        "phone": "+91 98765 43210",
        "auth_provider": "google",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        "pfp_type": "google",
        "role": "Agronomist & Lead Grower",
        "farm_name": "Bengal Precision Farmstead",
        "location": "Kolkata, WB",
        "acres": 42.5,
        "primary_crops": ["Rice", "Tomato", "Wheat"]
    }
}

OTP_STORE = {}

# Pydantic Schemas
class GoogleAuthRequest(BaseModel):
    credential: Optional[str] = None
    email: Optional[str] = "rishu.singh@gmail.com"
    name: Optional[str] = "Rishu Kumar Singh"
    picture: Optional[str] = None

class EmailAuthRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    avatar: Optional[str] = None

class PhoneAuthRequest(BaseModel):
    phone: str
    otp: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None

class YieldPredictRequest(BaseModel):
    rainfall_mm: float = 120.0
    avg_temp_c: float = 27.0
    humidity_pct: float = 71.0
    soil_ph: float = 6.5
    nitrogen_kg_ha: float = 72.0
    phosphorus_kg_ha: float = 45.0
    potassium_kg_ha: float = 60.0
    irrigation_mm: float = 80.0
    days_from_last_harvest: float = 30.0
    pest_index: float = 10.0
    soil_type: str = "Loamy"
    crop_type: str = "Rice"
    fertilized: str = "Yes"
    weather_zone: str = "Humid"
    seed_quality: str = "High"
    irrigation_method: str = "Flood"
    season: str = "Kharif"

class LSTMTrendRequest(BaseModel):
    crop: str = "Rice"
    current_health: float = 92.0
    current_yield: float = 8.5
    risk_score: float = 18.0
    soil_nitrogen: float = 72.0
    days_back: int = 7
    forecast_days: int = 14
    api_key: Optional[str] = None

class GANReportRequest(BaseModel):
    crop: str = "Tomato"
    disease: str = "Late Blight"
    confidence: float = 99.2
    health_score: float = 64.0
    yield_prediction: float = 5.2
    risk_level: str = "Moderate Risk"
    soil_npk: str = "72-45-60"
    location: str = "Kolkata, WB"
    season: str = "Kharif"
    farmer_name: str = "Rishu Kumar Singh"
    spectral_stress: float = 50.0


# ---------------- API ROUTES ----------------

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "service": "AgriVision AI Unified Backend",
        "models_loaded": {
            "disease_efficientnet": True,
            "crop_yield_mlp": True,
            "hyperleaf_spectral": True,
            "lstm_trend_forecaster": True,
            "gan_report_synthesizer": True,
            "image_validator": True
        },
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# 1. Presets for Instant 1-Click Parameter Scenarios
@app.get("/api/presets")
def get_presets():
    return {
        "presets": [
            {
                "id": "tomato_greenhouse",
                "name": "Tomato Precision Greenhouse",
                "crop_type": "Tomato",
                "season": "Rabi",
                "soil_type": "Loamy",
                "fertilized": "Yes",
                "weather_zone": "Temperate",
                "seed_quality": "High",
                "irrigation_method": "Drip",
                "rainfall_mm": 45.0,
                "avg_temp_c": 24.0,
                "humidity_pct": 65.0,
                "soil_ph": 6.2,
                "nitrogen_kg_ha": 95.0,
                "phosphorus_kg_ha": 55.0,
                "potassium_kg_ha": 80.0,
                "irrigation_mm": 100.0,
                "days_from_last_harvest": 25.0,
                "pest_index": 5.0,
                "location": "Kolkata, WB",
                "default_leaf": "/outputs/sample_leaves/tomato_late_blight.jpg"
            },
            {
                "id": "kharif_rice_basin",
                "name": "Kharif Rice Basin",
                "crop_type": "Rice",
                "season": "Kharif",
                "soil_type": "Clay",
                "fertilized": "Yes",
                "weather_zone": "Humid",
                "seed_quality": "High",
                "irrigation_method": "Flood",
                "rainfall_mm": 180.0,
                "avg_temp_c": 30.0,
                "humidity_pct": 82.0,
                "soil_ph": 6.8,
                "nitrogen_kg_ha": 78.0,
                "phosphorus_kg_ha": 35.0,
                "potassium_kg_ha": 60.0,
                "irrigation_mm": 80.0,
                "days_from_last_harvest": 30.0,
                "pest_index": 12.0,
                "location": "Kolkata, WB",
                "default_leaf": "/outputs/sample_leaves/tomato_healthy.jpg"
            },
            {
                "id": "apple_orchard",
                "name": "High-Altitude Apple Orchard",
                "crop_type": "Apple",
                "season": "Rabi",
                "soil_type": "Loamy",
                "fertilized": "Yes",
                "weather_zone": "Temperate",
                "seed_quality": "High",
                "irrigation_method": "Sprinkler",
                "rainfall_mm": 85.0,
                "avg_temp_c": 18.0,
                "humidity_pct": 58.0,
                "soil_ph": 6.5,
                "nitrogen_kg_ha": 60.0,
                "phosphorus_kg_ha": 40.0,
                "potassium_kg_ha": 70.0,
                "irrigation_mm": 60.0,
                "days_from_last_harvest": 60.0,
                "pest_index": 8.0,
                "location": "Himachal Pradesh",
                "default_leaf": "/outputs/sample_leaves/apple_scab.jpg"
            },
            {
                "id": "maize_agrofield",
                "name": "Commercial Maize Field",
                "crop_type": "Maize",
                "season": "Kharif",
                "soil_type": "Silty",
                "fertilized": "Yes",
                "weather_zone": "Tropical",
                "seed_quality": "Medium",
                "irrigation_method": "Rainfed",
                "rainfall_mm": 110.0,
                "avg_temp_c": 28.0,
                "humidity_pct": 70.0,
                "soil_ph": 6.4,
                "nitrogen_kg_ha": 120.0,
                "phosphorus_kg_ha": 60.0,
                "potassium_kg_ha": 50.0,
                "irrigation_mm": 40.0,
                "days_from_last_harvest": 45.0,
                "pest_index": 15.0,
                "location": "Bihar",
                "default_leaf": "/outputs/sample_leaves/corn_rust.jpg"
            }
        ]
    }

# 2. Sample Images with Real Test Dataset Leaves
@app.get("/api/sample-images")
def get_sample_images():
    samples = [
        {
            "id": "tomato_late_blight",
            "name": "Tomato Late Blight (Phytophthora infestans)",
            "crop": "Tomato",
            "expected_disease": "Tomato Late Blight",
            "url": "/outputs/sample_leaves/tomato_late_blight.jpg",
            "is_leaf": True,
            "category": "Fungal Oomycete"
        },
        {
            "id": "tomato_healthy",
            "name": "Healthy Tomato Foliage (Optimal Phenotype)",
            "crop": "Tomato",
            "expected_disease": "Healthy Foliage",
            "url": "/outputs/sample_leaves/tomato_healthy.jpg",
            "is_leaf": True,
            "category": "Optimal Phenotype"
        },
        {
            "id": "tomato_yellow_curl",
            "name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
            "crop": "Tomato",
            "expected_disease": "Yellow Leaf Curl",
            "url": "/outputs/sample_leaves/tomato_yellow_curl.jpg",
            "is_leaf": True,
            "category": "Viral Pathogen"
        },
        {
            "id": "apple_scab",
            "name": "Apple Scab Lesion (Venturia inaequalis)",
            "crop": "Apple",
            "expected_disease": "Apple Scab",
            "url": "/outputs/sample_leaves/apple_scab.jpg",
            "is_leaf": True,
            "category": "Fungal Ascomycete"
        },
        {
            "id": "corn_rust",
            "name": "Corn Common Rust (Puccinia sorghi)",
            "crop": "Maize",
            "expected_disease": "Common Rust",
            "url": "/outputs/sample_leaves/corn_rust.jpg",
            "is_leaf": True,
            "category": "Fungal Basidiomycete"
        },
        {
            "id": "non_leaf_sample",
            "name": "Non-Leaf Object (Validation Test Negative Control)",
            "crop": "Unknown",
            "expected_disease": "Rejection Expected",
            "url": "/outputs/sample_leaves/non_leaf_sample.jpg",
            "is_leaf": False,
            "category": "Negative Control"
        }
    ]
    return {"samples": samples}

# 3. Auth Endpoints
@app.post("/api/auth/google")
def auth_google(req: GoogleAuthRequest):
    email = req.email.strip().lower()
    default_pfp = req.picture or "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
    
    if email not in USERS_DB:
        USERS_DB[email] = {
            "id": f"usr-g-{uuid.uuid4().hex[:8]}",
            "name": req.name or email.split("@")[0].capitalize(),
            "email": email,
            "phone": "+91 98765 00000",
            "auth_provider": "google",
            "avatar": default_pfp,
            "pfp_type": "google",
            "role": "Farm Manager",
            "farm_name": "AgriVision Partner Farm",
            "location": "Kolkata, WB",
            "acres": 35.0,
            "primary_crops": ["Rice", "Tomato", "Wheat"]
        }
    else:
        if req.picture:
            USERS_DB[email]["avatar"] = req.picture
            
    user = USERS_DB[email]
    return {
        "success": True,
        "token": f"jwt-agri-{uuid.uuid4().hex}",
        "user": user
    }

@app.post("/api/auth/signup")
def auth_signup(req: EmailAuthRequest):
    email = req.email.strip().lower()
    if email in USERS_DB:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    avatar = req.avatar or f"https://api.dicebear.com/7.x/bottts/svg?seed={email}"
    user = {
        "id": f"usr-mail-{uuid.uuid4().hex[:8]}",
        "name": req.name or email.split("@")[0].capitalize(),
        "email": email,
        "phone": "+91 90000 00000",
        "auth_provider": "email",
        "avatar": avatar,
        "pfp_type": "custom",
        "role": "Precision Farmer",
        "farm_name": "Green Fields Estate",
        "location": "Kolkata, WB",
        "acres": 25.0,
        "primary_crops": ["Tomato", "Rice", "Maize"]
    }
    USERS_DB[email] = user
    return {"success": True, "token": f"jwt-agri-{uuid.uuid4().hex}", "user": user}

@app.post("/api/auth/login")
def auth_login(req: EmailAuthRequest):
    email = req.email.strip().lower()
    if email not in USERS_DB:
        avatar = req.avatar or f"https://api.dicebear.com/7.x/bottts/svg?seed={email}"
        USERS_DB[email] = {
            "id": f"usr-mail-{uuid.uuid4().hex[:8]}",
            "name": req.name or email.split("@")[0].capitalize(),
            "email": email,
            "phone": "+91 90000 00000",
            "auth_provider": "email",
            "avatar": avatar,
            "pfp_type": "custom",
            "role": "Farm Operator",
            "farm_name": "EcoSmart Agro",
            "location": "Kolkata, WB",
            "acres": 20.0,
            "primary_crops": ["Rice", "Tomato"]
        }
    user = USERS_DB[email]
    return {"success": True, "token": f"jwt-agri-{uuid.uuid4().hex}", "user": user}

@app.post("/api/auth/otp/send")
def send_otp(req: PhoneAuthRequest):
    phone = req.phone.strip()
    otp_code = "7729" # deterministic demo OTP for instant usability
    OTP_STORE[phone] = otp_code
    return {"success": True, "message": f"Verification code sent to {phone}", "demo_otp": otp_code}

@app.post("/api/auth/otp/verify")
def verify_otp(req: PhoneAuthRequest):
    phone = req.phone.strip()
    if req.otp != "7729" and req.otp != OTP_STORE.get(phone):
        raise HTTPException(status_code=400, detail="Invalid OTP verification code.")
    
    email_key = f"{phone.replace(' ', '').replace('+', '')}@mobile.agri"
    if email_key not in USERS_DB:
        USERS_DB[email_key] = {
            "id": f"usr-ph-{uuid.uuid4().hex[:8]}",
            "name": req.name or "Rishu Kumar Singh",
            "email": email_key,
            "phone": phone,
            "auth_provider": "phone",
            "avatar": req.avatar or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            "pfp_type": "phone",
            "role": "Agriculturalist",
            "farm_name": "Bengal Precision Farmstead",
            "location": "Kolkata, WB",
            "acres": 42.5,
            "primary_crops": ["Rice", "Tomato"]
        }
    user = USERS_DB[email_key]
    return {"success": True, "token": f"jwt-agri-{uuid.uuid4().hex}", "user": user}

@app.get("/api/user/profile")
def get_user_profile(email: Optional[str] = "rishu@agrivision.ai"):
    email = email.strip().lower()
    user = USERS_DB.get(email, next(iter(USERS_DB.values())))
    return {"user": user}

@app.put("/api/user/profile")
def update_user_profile(profile: Dict[str, Any] = Body(...)):
    email = profile.get("email", "").strip().lower()
    if not email:
        email = "rishu@agrivision.ai"
    if email in USERS_DB:
        USERS_DB[email].update(profile)
        return {"success": True, "user": USERS_DB[email]}
    USERS_DB[email] = profile
    return {"success": True, "user": USERS_DB[email]}


# 4. UNIFIED COMPLETE FARM & DISEASE INTELLIGENCE ANALYSIS (Matching dashboard_modified.py)
@app.post("/api/disease/detect")
@app.post("/api/farm/analyze")
async def analyze_farm_and_disease(
    file: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None),
    crop_type: Optional[str] = Form("Tomato"),
    season: Optional[str] = Form("Kharif"),
    soil_type: Optional[str] = Form("Loamy"),
    fertilized: Optional[str] = Form("Yes"),
    weather_zone: Optional[str] = Form("Humid"),
    seed_quality: Optional[str] = Form("High"),
    irrigation_method: Optional[str] = Form("Drip"),
    rainfall_mm: Optional[float] = Form(120.0),
    avg_temp_c: Optional[float] = Form(27.0),
    humidity_pct: Optional[float] = Form(71.0),
    soil_ph: Optional[float] = Form(6.5),
    nitrogen_kg_ha: Optional[float] = Form(72.0),
    phosphorus_kg_ha: Optional[float] = Form(45.0),
    potassium_kg_ha: Optional[float] = Form(60.0),
    irrigation_mm: Optional[float] = Form(80.0),
    days_from_last_harvest: Optional[float] = Form(30.0),
    pest_index: Optional[float] = Form(10.0),
    farmer_name: Optional[str] = Form("Rishu Kumar Singh"),
    location: Optional[str] = Form("Kolkata, WB")
):
    """
    Executes the complete unified intelligence pipeline from dashboard_modified.py:
    1. Image Validation (green ratio, vegetation ratio)
    2. Neural MLP Yield Prediction (predict_crop_yield)
    3. Deep CNN Disease Detection (predict_disease)
    4. HyperLeaf Spectral Model (predict_spectral if TIFF)
    5. Spectral Stress Analysis (preprocess_leaf_image, analyze_leaf_spectrum)
    6. Stress Visualization (generate_stress_visualization -> heatmap, overlay, marked leaf)
    7. Crop Consistency Validation (farm crop vs detected disease crop)
    8. Composite Crop Health Score (calculate_health_score)
    9. Composite Farm Risk Engine (calculate_risk)
    10. 14-Day Recurrent Forecast (generate_forecast)
    11. Prioritized Agronomic Recommendations (generate_recommendations)
    12. Agri-GAN Generative Dossier (generate_gan_report)
    """
    
    # 1. Determine leaf image source
    saved_path = None
    image_web_url = None
    is_tiff = False
    
    if file and file.filename:
        file_ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
        unique_fn = f"leaf_{uuid.uuid4().hex[:10]}{file_ext}"
        saved_path = os.path.join(UPLOAD_DIR, unique_fn)
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_web_url = f"/outputs/web_uploads/{unique_fn}"
        if file_ext in (".tif", ".tiff"):
            is_tiff = True
    elif sample_id:
        # Check sample files
        sample_path = os.path.join(SAMPLES_DIR, f"{sample_id}.jpg")
        if not os.path.exists(sample_path):
            sample_path = os.path.join(SAMPLES_DIR, "tomato_late_blight.jpg")
        saved_path = sample_path
        image_web_url = f"/outputs/sample_leaves/{os.path.basename(sample_path)}"
    else:
        # Default fallback sample
        saved_path = os.path.join(SAMPLES_DIR, "tomato_late_blight.jpg")
        image_web_url = "/outputs/sample_leaves/tomato_late_blight.jpg"

    try:
        # STEP 1: VALIDATE IMAGE
        validation_result = validate_crop_image(saved_path)
        
        # If image validation failed (e.g. non-leaf object uploaded), reject early like dashboard_modified.py
        if not validation_result.get("valid", True):
            return {
                "success": False,
                "validation_failed": True,
                "uploaded_image": image_web_url,
                "validation": {
                    "valid": False,
                    "status": "IMAGE VALIDATION FAILED",
                    "reason": validation_result.get("reason", "Uploaded image does not appear to contain a crop leaf."),
                    "green_ratio": round(float(validation_result.get("green_ratio", 0.0)) * 100, 2),
                    "vegetation_ratio": round(float(validation_result.get("vegetation_ratio", 0.0)) * 100, 2),
                    "brightness": round(float(validation_result.get("brightness", 0.0)), 1)
                },
                "message": "Image validation failed. The uploaded image does not appear to contain a crop or leaf."
            }

        # STEP 2: NEURAL YIELD PREDICTION
        yield_pred_val = predict_crop_yield(
            rainfall_mm=float(rainfall_mm),
            avg_temp_c=float(avg_temp_c),
            humidity_pct=float(humidity_pct),
            soil_ph=float(soil_ph),
            nitrogen_kg_ha=float(nitrogen_kg_ha),
            phosphorus_kg_ha=float(phosphorus_kg_ha),
            potassium_kg_ha=float(potassium_kg_ha),
            irrigation_mm=float(irrigation_mm),
            days_from_last_harvest=float(days_from_last_harvest),
            pest_index=float(pest_index),
            soil_type=str(soil_type),
            crop_type=str(crop_type),
            fertilized=str(fertilized),
            weather_zone=str(weather_zone),
            seed_quality=str(seed_quality),
            irrigation_method=str(irrigation_method),
            season=str(season).split()[0] if season else "Kharif"
        )
        
        yield_pred_tons = float(yield_pred_val)
        if yield_pred_tons < 2.0:
            yield_cat = "Low"
        elif yield_pred_tons < 4.0:
            yield_cat = "Moderate"
        elif yield_pred_tons < 6.0:
            yield_cat = "Good"
        else:
            yield_cat = "High"

        # STEP 3: DEEP CNN DISEASE DETECTION
        disease_result = predict_disease(saved_path)
        detected_crop = str(disease_result.get("crop", crop_type))
        raw_disease = str(disease_result.get("disease", "healthy"))
        confidence = float(disease_result.get("confidence", 95.0))
        disease_status = str(disease_result.get("status", "Diseased" if "healthy" not in raw_disease.lower() else "Healthy"))
        
        # Clean human-friendly disease title
        clean_disease_name = raw_disease.replace("Tomato___", "").replace("Apple___", "").replace("Corn_(maize)___", "").replace("Potato___", "").replace("_", " ")

        # Format Top 3 Predictions
        formatted_top3 = []
        for p in disease_result.get("top_predictions", [])[:3]:
            p_class = str(p.get("class", ""))
            p_clean = p_class.replace("Tomato___", "").replace("Apple___", "").replace("Corn_(maize)___", "").replace("Potato___", "").replace("_", " ")
            formatted_top3.append({
                "class_raw": p_class,
                "class_name": p_clean,
                "crop": p.get("crop", detected_crop),
                "confidence": round(float(p.get("confidence", 0.0)), 2),
                "healthy": p.get("healthy", False)
            })

        # STEP 4: HYPERLEAF SPECTRAL MODEL (if TIFF)
        hyperleaf_result = None
        if is_tiff:
            try:
                hl_raw = predict_spectral(saved_path)
                hyperleaf_result = {
                    "spectral_bands": hl_raw.get("spectral_bands", 128),
                    "grain_weight": round(float(hl_raw.get("grain_weight", 0.0)), 4),
                    "gsw": round(float(hl_raw.get("gsw", 0.0)), 6),
                    "phi_ps2": round(float(hl_raw.get("phi_ps2", 0.0)), 6)
                }
            except Exception as e:
                print("HyperLeaf spectral run error:", e)

        # STEP 5: SPECTRAL STRESS ANALYSIS
        processed_image = preprocess_leaf_image(saved_path)
        spectral_raw = analyze_leaf_spectrum(processed_image)
        spectral_analysis = spectral_raw.get("analysis", {})
        spectral_stress = float(spectral_analysis.get("spectral_stress_score", 15.0))

        # STEP 6: STRESS VISUALIZATIONS
        vis_paths = generate_stress_visualization(saved_path)
        heatmap_rel = os.path.relpath(vis_paths.get("heatmap_path", ""), BASE_DIR).replace("\\", "/") if vis_paths.get("heatmap_path") else ""
        overlay_rel = os.path.relpath(vis_paths.get("overlay_path", ""), BASE_DIR).replace("\\", "/") if vis_paths.get("overlay_path") else ""
        marked_rel = os.path.relpath(vis_paths.get("marked_path", ""), BASE_DIR).replace("\\", "/") if vis_paths.get("marked_path") else ""

        # STEP 7: CROP CONSISTENCY VERIFICATION
        crop_match = crop_type.lower().strip() == detected_crop.lower().strip()

        # STEP 8: COMPOSITE CROP HEALTH SCORE
        health_raw = calculate_health_score(
            yield_value=yield_pred_tons,
            yield_category=yield_cat,
            disease=raw_disease,
            disease_confidence=confidence,
            crop_consistency=crop_match,
            pest_index=float(pest_index),
            humidity_pct=float(humidity_pct),
            soil_ph=float(soil_ph),
            spectral_stress=spectral_stress
        )
        health_score = float(health_raw.get("health_score", 85.0))
        health_status = str(health_raw.get("health_status", "Good"))

        # STEP 9: COMPOSITE RISK ENGINE
        risk_raw = calculate_risk(
            disease=raw_disease,
            disease_confidence=confidence,
            yield_category=yield_cat,
            pest_index=float(pest_index),
            humidity_pct=float(humidity_pct),
            crop_consistency=crop_match,
            spectral_stress=spectral_stress
        )
        risk_score = float(risk_raw.get("overall_risk_score", 20.0))
        risk_level = str(risk_raw.get("risk_level", "Low Risk"))

        # STEP 10: 14-DAY RECURRENT FORECAST
        forecast_raw = generate_forecast(
            current_yield=yield_pred_tons,
            yield_category=yield_cat,
            disease_risk=risk_score,
            health_score=health_score,
            forecast_days=14
        )

        # STEP 11: PRIORITIZED AGRONOMIC RECOMMENDATIONS
        rec_raw = generate_recommendations(
            crop=detected_crop,
            disease=raw_disease,
            disease_confidence=confidence,
            yield_category=yield_cat,
            health_score=health_score,
            health_status=health_status,
            risk_level=risk_level,
            pest_index=float(pest_index),
            humidity_pct=float(humidity_pct),
            soil_ph=float(soil_ph),
            spectral_stress=spectral_stress
        )

        # STEP 12: PRE-GENERATE AGRI-GAN 2.0 RECOVERY DOSSIER
        gan_report_data = generate_gan_report(
            crop=detected_crop,
            disease=clean_disease_name,
            confidence=round(confidence, 1),
            health_score=round(health_score, 1),
            yield_prediction=round(yield_pred_tons, 2),
            risk_level=risk_level,
            soil_npk=f"{int(nitrogen_kg_ha)}-{int(phosphorus_kg_ha)}-{int(potassium_kg_ha)}",
            location=location,
            season=season,
            farmer_name=farmer_name,
            spectral_stress=round(spectral_stress, 1)
        )

        # BUILD UNIFIED COMPLETE RESPONSE
        return {
            "success": True,
            "validation_failed": False,
            "uploaded_image": image_web_url,
            "timestamp": time.strftime("%b %d, %Y • %I:%M %p"),
            
            # Farm parameters echoed back
            "farm_parameters": {
                "crop_type": crop_type,
                "season": season,
                "soil_type": soil_type,
                "fertilized": fertilized,
                "weather_zone": weather_zone,
                "seed_quality": seed_quality,
                "irrigation_method": irrigation_method,
                "rainfall_mm": rainfall_mm,
                "avg_temp_c": avg_temp_c,
                "humidity_pct": humidity_pct,
                "soil_ph": soil_ph,
                "nitrogen_kg_ha": nitrogen_kg_ha,
                "phosphorus_kg_ha": phosphorus_kg_ha,
                "potassium_kg_ha": potassium_kg_ha,
                "irrigation_mm": irrigation_mm,
                "days_from_last_harvest": days_from_last_harvest,
                "pest_index": pest_index
            },

            # 1. Image Validation
            "image_validation": {
                "status": "VERIFIED",
                "valid": True,
                "green_ratio": round(float(validation_result.get("green_ratio", 0.0)) * 100, 2),
                "vegetation_ratio": round(float(validation_result.get("vegetation_ratio", 0.0)) * 100, 2),
                "brightness": round(float(validation_result.get("brightness", 0.0)), 1),
                "reason": validation_result.get("reason", "Valid vegetation canopy detected.")
            },

            # 2. Yield Intelligence
            "yield_intelligence": {
                "predicted_yield_tons_per_ha": round(yield_pred_tons, 3),
                "yield_category": yield_cat,
                "crop": crop_type,
                "status": "Calculated via trained Multi-Layer Perceptron"
            },

            # 3. Disease Intelligence
            "disease_intelligence": {
                "detected_crop": detected_crop,
                "disease_raw": raw_disease,
                "disease_name": clean_disease_name,
                "confidence": round(confidence, 1),
                "status": disease_status,
                "healthy": "healthy" in raw_disease.lower(),
                "category": "Optimal Phenotype" if "healthy" in raw_disease.lower() else ("Viral Infection" if "virus" in raw_disease.lower() else "Fungal Pathology"),
                "top_predictions": formatted_top3
            },

            # 4. Crop Consistency Verification
            "crop_consistency": {
                "is_match": crop_match,
                "status": "VERIFIED" if crop_match else "WARNING",
                "farm_crop": crop_type,
                "detected_crop": detected_crop,
                "message": "Farm crop and detected leaf match perfectly." if crop_match else f"WARNING: Farm registered crop is '{crop_type}', but uploaded leaf is identified as '{detected_crop}'!"
            },

            # 5. Spectral Intelligence
            "spectral_intelligence": {
                "spectral_stress_score": round(spectral_stress, 1),
                "stress_level": spectral_analysis.get("stress_level", "Normal"),
                "vegetation_condition": spectral_analysis.get("vegetation_condition", "Healthy"),
                "discoloration_level": spectral_analysis.get("discoloration_level", "Low"),
                "tissue_damage_level": spectral_analysis.get("tissue_damage_level", "None"),
                "vegetation_index_ndi": round(float(spectral_analysis.get("vegetation_index", 0.0)), 4),
                "excess_green_index_exg": round(float(spectral_analysis.get("excess_green_index", 0.0)), 2),
                "green_ratio": round(float(spectral_analysis.get("green_ratio", 0.0)), 4),
                "saturation": round(float(spectral_analysis.get("saturation", 0.0)), 2)
            },

            # 6. Stress Visualizations
            "visualizations": {
                "marked_leaf_url": f"/{marked_rel}" if marked_rel else image_web_url,
                "heatmap_url": f"/{heatmap_rel}" if heatmap_rel else "",
                "overlay_url": f"/{overlay_rel}" if overlay_rel else "",
                "average_stress": round(float(vis_paths.get("average_stress", spectral_stress)), 2),
                "stress_level": vis_paths.get("stress_level", "Normal"),
                "affected_area_percentage": round(float(vis_paths.get("affected_area_percentage", 0.0)), 2),
                "num_stressed_regions": int(vis_paths.get("num_stressed_regions", 0))
            },

            # 7. HyperLeaf Spectral Result (if TIFF)
            "hyperleaf_spectral": hyperleaf_result,

            # 8. Crop Health Score
            "health_intelligence": {
                "health_score": round(health_score, 1),
                "health_status": health_status,
                "breakdown": health_raw.get("breakdown", {})
            },

            # 9. Risk Analysis
            "risk_intelligence": {
                "overall_risk_score": round(risk_score, 1),
                "risk_level": risk_level,
                "disease_risk": round(float(risk_raw.get("disease_risk", 0.0)), 1),
                "pest_risk": round(float(risk_raw.get("pest_risk", 0.0)), 1),
                "environmental_risk": round(float(risk_raw.get("environmental_risk", 0.0)), 1),
                "yield_risk": round(float(risk_raw.get("yield_risk", 0.0)), 1),
                "breakdown": risk_raw.get("breakdown", {})
            },

            # 10. Multi-Horizon Forecast
            "forecast_intelligence": {
                "forecast_days": int(forecast_raw.get("forecast_days", 14)),
                "current_yield": round(float(forecast_raw.get("current_yield", yield_pred_tons)), 3),
                "projected_yield": round(float(forecast_raw.get("projected_yield", yield_pred_tons)), 3),
                "projected_disease_risk": round(float(forecast_raw.get("projected_disease_risk", risk_score)), 1),
                "future_risk_level": forecast_raw.get("future_risk_level", risk_level),
                "forecast_type": forecast_raw.get("forecast_type", "Analytical Recurrent Extrapolation"),
                "daily_trend": forecast_raw.get("daily_trend", [])
            },

            # 11. Recommendations
            "recommendation_intelligence": {
                "priority_areas": rec_raw.get("priority_areas", ["Crop Vigor Optimization"]),
                "recommendations": rec_raw.get("recommendations", ["Maintain optimal fertigation regimen and scout canopy regularly."]),
                "summary": rec_raw.get("summary", "Field conditions are within manageable agronomic parameters.")
            },

            # 12. Agri-GAN 2.0 Dossier
            "gan_dossier": gan_report_data
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# 5. Standalone Yield Endpoint
@app.post("/api/yield/predict")
def predict_yield_standalone(req: YieldPredictRequest):
    try:
        val = predict_crop_yield(
            rainfall_mm=req.rainfall_mm,
            avg_temp_c=req.avg_temp_c,
            humidity_pct=req.humidity_pct,
            soil_ph=req.soil_ph,
            nitrogen_kg_ha=req.nitrogen_kg_ha,
            phosphorus_kg_ha=req.phosphorus_kg_ha,
            potassium_kg_ha=req.potassium_kg_ha,
            irrigation_mm=req.irrigation_mm,
            days_from_last_harvest=req.days_from_last_harvest,
            pest_index=req.pest_index,
            soil_type=req.soil_type,
            crop_type=req.crop_type,
            fertilized=req.fertilized,
            weather_zone=req.weather_zone,
            seed_quality=req.seed_quality,
            irrigation_method=req.irrigation_method,
            season=req.season
        )
        cat = "High" if val >= 6.0 else "Good" if val >= 4.0 else "Moderate" if val >= 2.0 else "Low"
        return {"predicted_yield_t_ha": round(val, 3), "category": cat, "crop": req.crop_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 6. Deep Recurrent LSTM Trend Engine
@app.post("/api/lstm/forecast")
def lstm_forecast_endpoint(req: LSTMTrendRequest):
    try:
        trends = run_lstm_trend_analysis(
            crop=req.crop,
            current_health=req.current_health,
            current_yield=req.current_yield,
            risk_score=req.risk_score,
            soil_nitrogen=req.soil_nitrogen,
            days_back=req.days_back,
            forecast_days=req.forecast_days,
            gemini_api_key=req.api_key
        )
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 7. Agri-GAN 2.0 Report Synthesizer Endpoint
@app.post("/api/gan/generate-report")
def gan_report_endpoint(req: GANReportRequest):
    try:
        report = generate_gan_report(
            crop=req.crop,
            disease=req.disease,
            confidence=req.confidence,
            health_score=req.health_score,
            yield_prediction=req.yield_prediction,
            risk_level=req.risk_level,
            soil_npk=req.soil_npk,
            location=req.location,
            season=req.season,
            farmer_name=req.farmer_name,
            spectral_stress=req.spectral_stress
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount Frontend static assets and SPA fallback
if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("outputs/"):
            raise HTTPException(status_code=404, detail="Not Found")
        target_file = os.path.join(FRONTEND_DIST, full_path)
        if os.path.isfile(target_file):
            return FileResponse(target_file)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
