# AgriVision AI — Data Flow Specification & DFD Analysis

## 1. Overview & Data Flow Principles

This document specifies how raw data (user credentials, mobile leaf uploads, soil chemistry inputs, and meteorological readings) enters, travels through, is transformed by, and is returned from the AgriVision AI system.

> 🖼️ **High-Resolution Visual Diagram Assets:**
> - Core Dataflow (PNG): [`core_dataflow_breakdown.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/core_dataflow_breakdown.png) | (JPG): [`core_dataflow_breakdown.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/core_dataflow_breakdown.jpg)
> - DFD Level 0 Context (PNG): [`dfd_0.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/dfd_0.png) | (JPG): [`dfd_0.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/dfd_0.jpg)
> - DFD Level 1 Detailed (PNG): [`dfd_1.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/dfd_1.png) | (JPG): [`dfd_1.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/dfd_1.jpg)
> - End-to-End Pipeline Analysis (PNG): [`data_flow_analysis.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/data_flow_analysis.png) | (JPG): [`data_flow_analysis.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/data_flow_analysis.jpg)
> - Mermaid Sources: [`dfd_level_0.mmd`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/dfd_level_0.mmd) & [`dfd_level_1.mmd`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/dfd_level_1.mmd)

The system processes two primary data streams:
1. **Unstructured Binary Stream:** Crop foliage photographs processed through computer vision algorithms and deep convolutional neural networks.
2. **Structured Multivariate Stream:** Tabular agronomic parameters (N-P-K, pH, humidity, rainfall) processed through feature transformers, multi-layer perceptrons, recurrent sequence forecasters, and scoring engines.

---

## 2. DFD Level 0 — Context Diagram (System Overview)

The Level 0 Context Diagram depicts the entire AgriVision AI platform as a single centralized processing system interacting with external entities.

```
                  ┌──────────────────────────────────────────┐
                  │          FARMER / AGRONOMIST             │
                  │             (User Entity)                │
                  └─────────────┬────────────────────────────┘
                                │
     [User Credentials / Auth]  │  ▲ [User Profile, Dashboard Data]
     [Foliar Leaf Images]       │  │ [Disease Diagnostics, Heatmaps]
     [Soil / Weather Parameters]│  │ [Yield Forecasts, Treatment Plans]
     [Profile Updates / Key]    │  │ [Printable GAN Dossiers]
                                ▼  │
                  ┌──────────────────────────────────────────┐
                  │                 [ 0.0 ]                  │
                  │             AGRIVISION AI                │
                  │          UNIFIED PLATFORM                │
                  └──────────────┬───────────────┬───────────┘
                                 │               │
  [Pre-Trained Weights, Scalers] │ ▲             │ ▲ [Prompt JSON]
  [Persisted Web Uploads]        │ │ [Read/Write]│ │ [Recurrent Trajectory JSON]
  [Generated Heatmap Artifacts]  │ │             │ │
                                 ▼ │             ▼ │
                  ┌──────────────────────┐ ┌───────────────────────────┐
                  │  LOCAL FILESYSTEM    │ │  GOOGLE GEMINI API        │
                  │     DATA STORE       │ │  (External Neural Svc)    │
                  └──────────────────────┘ └───────────────────────────┘
```

### Level 0 Entity Interactions
- **Farmer / Agronomist:** Submits identity credentials, captures/uploads leaf photos, adjusts farm parameters, and receives diagnostic cards, risk scores, LSTM trajectories, and downloadable dossiers.
- **Local Filesystem Data Store:** Provides serialized neural weights (`.keras`) and Scikit-learn scalers (`.pkl`); stores uploaded photos and generated heatmaps/overlays.
- **Google Gemini API (External):** Receives structured agronomic prompt JSON containing recent historical farm vectors and returns predicted recurrent LSTM sequence dynamics.

---

## 3. DFD Level 1 — Detailed Process Decomposition

The Level 1 Data Flow Diagram breaks AgriVision AI into its core functional sub-processes, data stores, and intermediate transforms.

```
[User / Client]
       │
       │ (1. Auth Payload)
       ▼
 ┌───────────┐
 │ Process 1 │ ─── [Read/Write User Data] ───► ┌────────────────────────┐
 │   Auth    │ ◄── [User Record / Token]  ───  │ Data Store 1: USERS_DB │
 │ Controller│                                 └────────────────────────┘
 └─────┬─────┘
       │ (Profile & Token Response)
       ▼
[User Authenticated]
       │
       │ (2. Multipart Leaf Image Upload + Form Parameters)
       ▼
 ┌───────────┐
 │ Process 2 │ ─── [Write Binary Image] ────► ┌────────────────────────┐
 │  Upload   │                                │ Data Store 2:          │
 │ Receiver  │ ◄── [Stored File Path]   ────  │ /outputs/web_uploads/  │
 └─────┬─────┘                                └────────────────────────┘
       │ (Image File Path)
       ▼
 ┌───────────┐
 │ Process 3 │
 │   Image   │ ──► [Invalid: Green < 1%] ──► [HTTP 400 Validation Error]
 │ Validator │
 └─────┬─────┘
       │ (Valid Image Path)
       ├─────────────────────────────────┬────────────────────────────────┐
       │                                 │                                │
       ▼                                 ▼                                ▼
 ┌───────────┐                     ┌───────────┐                    ┌───────────┐
 │ Process 4 │                     │ Process 5 │                    │ Process 6 │
 │  Disease  │                     │  Optical  │                    │   Yield   │
 │ Predictor │                     │ Stress    │                    │ Predictor │
 │(Efficient-│                     │ Visualizer│                    │  (MLP)    │
 │   Net)    │                     └─────┬─────┘                    └─────┬─────┘
 └─────┬─────┘                           │                                │
       │ (Disease, Conf, Crop)           │ (Heatmap / Overlay Path)       │ (Yield t/ha, Cat)
       │                                 ▼                                │
       │                           ┌───────────┐                          │
       │                           │Data Store │                          │
       │                           │3: Outputs │                          │
       │                           └───────────┘                          │
       │                                 │                                │
       └─────────────────┬───────────────┴────────────────────────────────┘
                         │
                         ▼
                   ┌───────────┐
                   │ Process 7 │ ◄── [Pest Index, Humidity, Soil pH]
                   │ Scoring & │
                   │ Composite │
                   │   Risk    │
                   └─────┬─────┘
                         │
                         ├────────────────────────────────────────┐
                         │ (Health Score, Status, Risk Level)     │
                         ▼                                        ▼
                   ┌───────────┐                            ┌───────────┐
                   │ Process 8 │                            │ Process 9 │
                   │  Advisory │                            │  14-Day   │
                   │  Engine   │                            │ Forecaster│
                   └─────┬─────┘                            └─────┬─────┘
                         │ (Actionable Recs)                      │ (Yield / Risk Curve)
                         ▼                                        ▼
                   ┌────────────────────────────────────────────────────┐
                   │        Aggregated Diagnostic JSON Payload          │
                   └─────────────────────┬──────────────────────────────┘
                                         │
                                         ▼
                                   [Client UI]
                                         │
                   ┌─────────────────────┴──────────────────────┐
                   │ (Fetch LSTM Trends)                        │ (Generate GAN Report)
                   ▼                                            ▼
             ┌───────────┐                                ┌───────────┐
             │Process 10 │                                │Process 11 │
             │   LSTM    │ ◄──► [Gemini API /             │ Agri-GAN  │
             │ Forecaster│       Native Fallback]         │Synthesizer│
             └─────┬─────┘                                └─────┬─────┘
                   │ (Multi-Horizon Projections)                │ (Dossier Data)
                   ▼                                            ▼
             [Trend Line & Bounds]                        [Printable PDF Dossier]
```

---

## 4. Step-by-Step Data Flow Explanation

### Stage 1: User Identity & Profile Ingestion
- **Origin:** Web browser user interface (`AuthModal.jsx`).
- **Receiver:** `api_server.py` auth route handlers (`/api/auth/google`, `/api/auth/login`, `/api/auth/signup`, `/api/auth/otp/verify`).
- **Processing:** Payload fields are deserialized into Pydantic models. For Google sign-in, existing records in `USERS_DB` are updated with the user's name, email, and Google profile picture (PFP). For email signup, collisions are checked before a new user object is generated. For phone OTP, verification code `7729` is validated against `OTP_STORE`.
- **Destination:** Returns a generated session token and structured user profile dictionary to `AppContext.jsx`.
- **Persistence:** Stored in memory (`USERS_DB`) and serialized to browser `localStorage` (`agrivision_user`).
- **Output:** Authenticated user session; avatar and name displayed across the navbar and dashboard banner.

### Stage 2: Diagnostic Leaf Image Upload & Storage
- **Origin:** Camera snapshot or file selector in `DiseaseView.jsx`.
- **Receiver:** `POST /api/disease/detect` in `api_server.py`.
- **Processing:** The raw stream is captured as `UploadFile`. A UUID filename (`leaf_{uuid}.jpg`) is generated. The binary file is read in chunks via `shutil.copyfileobj` and written to disk.
- **Destination:** File is saved to `outputs/web_uploads/{unique_filename}` and its path is passed to the validation module.
- **Persistence:** Stored permanently on the server filesystem.
- **Output:** Canonical file path string on server storage.

### Stage 3: Image Quality & Vegetation Ratio Verification
- **Origin:** Canonical file path from Stage 2.
- **Receiver:** `validate_crop_image()` in `intelligence/image_validation/validator.py`.
- **Processing:** 
  1. Image is decoded from disk using `cv2.imread()`.
  2. Resolution check verifies $\text{height} \ge 100$ and $\text{width} \ge 100$.
  3. Image is converted to HSV color space (`cv2.COLOR_BGR2HSV`).
  4. An in-range mask filters green chromatic pixels between HSV $[20, 30, 20]$ and $[100, 255, 255]$.
  5. The green ratio is computed:
     $$\text{Green Ratio} = \frac{\text{Green Pixels}}{\text{Total Image Pixels}}$$
  6. General vegetation pixels are evaluated ($\text{saturation} > 25$ and $\text{value} > 30$).
- **Destination:** If green ratio $< 1.0\%$, processing terminates with a descriptive validation error payload. If valid, the execution proceeds to model inference.
- **Output:** Validation status dictionary (`valid: True`, `green_ratio: float`, `vegetation_ratio: float`).

### Stage 4: Deep CNN Foliar Pathogen Inference
- **Origin:** Validated leaf image path.
- **Receiver:** `predict_disease()` in `module1/disease_detection/predict.py`.
- **Processing:**
  1. Checks if `_model` is cached; if not, loads `models/disease/disease_efficientnet.keras` via TensorFlow Keras `load_model()`.
  2. Loads class label dictionary from `models/disease/class_names.json`.
  3. Loads image with target resolution $(224, 224)$ via Keras `load_img()`.
  4. Converts PIL image to a 3D NumPy array via `img_to_array()` and expands dimensions to $(1, 224, 224, 3)$.
  5. Executes forward pass: `_model.predict(img_array, verbose=0)`.
  6. Applies Softmax argmax to determine predicted class index, extracts top candidate probabilities, and parses crop name and disease name.
- **Destination:** Prediction results transmitted to the diagnostic orchestrator in `api_server.py`.
- **Output:** Dictionary containing detected crop species, disease name, confidence score percentage, and top-3 prediction classes.

### Stage 5: Optical & Hyperspectral Stress Map Synthesis
- **Origin:** Validated leaf image path.
- **Receiver:** `generate_stress_visualization()` in `intelligence/spectral/visualizer.py`.
- **Processing:**
  1. Image is read via OpenCV and normalized to floating point RGB in range $[0.0, 1.0]$.
  2. Computes Excess Green Index: $ExG = 2.0g - r - b$.
  3. Computes Normalized Difference Greenness Index: $NDI = \frac{g - r}{g + r + 1e-8}$.
  4. Normalizes $ExG$ and $NDI$ arrays using 2nd and 98th percentile clipping.
  5. Converts normalized stress gradient into thermal colormap representation using OpenCV `cv2.applyColorMap(..., cv2.COLORMAP_JET)`.
  6. Computes morphological leaf edge contours and overlays boundary markings on the original RGB frame.
  7. Writes two artifact images to `outputs/spectral/`: `*_heatmap.jpg` and `*_overlay.jpg`.
  8. `analyze_leaf_spectrum()` computes numerical optical stress score (0–100 scale).
- **Destination:** Artifact paths saved to disk; relative web URLs returned to API orchestrator.
- **Persistence:** Written to `outputs/spectral/`.
- **Output:** Heatmap image, morphological overlay image, and numerical spectral stress index.

### Stage 6: Tabular MLP Crop Yield Forecasting
- **Origin:** Form parameters submitted in diagnostic request (or standalone from `YieldView.jsx`).
- **Receiver:** `predict_crop_yield()` in `module1/yield_prediction/predict.py`.
- **Processing:**
  1. Loads `crop_yield_mlp.keras` model and `preprocessor.pkl` column transformer.
  2. Assembles a single-row Pandas DataFrame containing 10 numerical features and 7 categorical features.
  3. Transformer executes One-Hot Encoding on categorical attributes and Standard Scaling on continuous variables.
  4. Executes neural forward pass: `model.predict(preprocessed_data, verbose=0)`.
  5. Classifies output into categorical yield tier:
     - $< 2.0\ t/ha \to \text{Low}$
     - $2.0 \le \text{yield} < 4.0\ t/ha \to \text{Moderate}$
     - $4.0 \le \text{yield} < 6.0\ t/ha \to \text{Good}$
     - $\ge 6.0\ t/ha \to \text{High}$
- **Destination:** Yield tonnage float and categorical rating passed to scoring engines.
- **Output:** Predicted crop yield in metric tons per hectare ($t/ha$) and qualitative category.

### Stage 7: Holistic Health & Composite Risk Engine Scoring
- **Origin:** Outputs from Stages 4, 5, and 6 along with soil pH, ambient humidity, and pest index.
- **Receiver:** `calculate_health_score()` and `calculate_risk()` in `intelligence/health/` and `intelligence/risk/`.
- **Processing:**
  1. **Health Score Calculation:**
     - Base score initialized at $100.0$.
     - Disease penalty deducted: up to $-40$ points based on confidence.
     - Yield penalty deducted: $-30$ (Low), $-18$ (Moderate), $-7$ (Good), $0$ (High).
     - Pest penalty deducted: up to $-15$ points.
     - Extreme humidity ($\ge 80\%$) and non-optimal soil pH ($< 5.5$ or $> 8.0$) penalties applied.
     - Crop inconsistency penalty: $-10$ points if declared crop does not match visual leaf model.
     - Optical spectral stress penalty: up to $-20$ points.
     - Clamped to $[0.0, 100.0]$ and categorized (Excellent, Healthy, Moderate, At Risk, Poor).
  2. **Composite Risk Calculation:**
     - Computes individual normalized sub-risks: disease risk, pest risk, environmental humidity risk, yield risk, consistency risk, and spectral risk.
     - Computes weighted sum:
       $$\text{Overall Risk} = 0.35 R_{\text{disease}} + 0.15 R_{\text{pest}} + 0.15 R_{\text{env}} + 0.15 R_{\text{yield}} + 0.05 R_{\text{cons}} + 0.15 R_{\text{spectral}}$$
     - Categorized into Critical ($\ge 75$), High ($\ge 55$), Moderate ($\ge 35$), Low ($\ge 15$), or Minimal ($< 15$).
- **Destination:** Scores routed to recommendation and forecast generators.
- **Output:** Standardized crop health score, health status, composite risk score, and risk tier.

### Stage 8: Recommendation & 14-Day Baseline Forecast Generation
- **Origin:** Diagnostic findings, health score, risk score, and environmental readings.
- **Receiver:** `generate_recommendations()` and `generate_forecast()` in `intelligence/recommendations/` and `intelligence/forecast/`.
- **Processing:**
  1. Priority matrix assigns treatments: Immediate chemical/fungicidal actions (0–48 hrs), Secondary micronutrient chelation (Days 3–5), and Preventative water/humidity controls (Days 7+).
  2. Evaluates historical yield moving average deltas to extrapolate projected yield and risk trends over a 14-day window.
- **Destination:** Aggregated into final diagnostic response dictionary by `api_server.py`.
- **Output:** Completed JSON response transmitted back to client via HTTP 200 OK.

### Stage 9: Deep Recurrent LSTM Trend Simulation
- **Origin:** User interaction in `LSTMTrendView.jsx` (or automatic background trend query).
- **Receiver:** `POST /api/lstm/forecast` $\to$ `run_lstm_trend_analysis()` in `lstm_trend_engine.py`.
- **Processing:**
  1. Checks for presence of `gemini_api_key` in request or server environment.
  2. If key exists: Assembles structured prompt detailing crop type, baseline health, yield, risk, and nitrogen index. Executes HTTPS POST request to Gemini API, enforcing strict JSON output representing recurrent sequence cell vectors.
  3. If key is absent or request times out: Reverts to deterministic recurrent LSTM mathematical formulas modeling cell state momentum ($c_t = f_t c_{t-1} + i_t \tilde{c}_t$) and calculating $\pm 1\sigma$ uncertainty envelopes.
  4. Flags temporal anomalies (e.g., Vapor Pressure Deficit band deviations, soil nitrogen assimilation trends).
- **Destination:** Returns sequence projections array to React frontend.
- **Output:** 7-day historical progression and multi-horizon future projection curve rendered via SVG.

### Stage 10: Generative Adversarial (GAN) Report Synthesis
- **Origin:** User trigger in `GANReportView.jsx`.
- **Receiver:** `POST /api/gan/generate-report` $\to$ `generate_gan_report()` in `gan_report_engine.py`.
- **Processing:**
  1. Generator $G(z \mid c)$ ingests conditioning vector (crop, pathogen, confidence, health score, spectral stress).
  2. Synthesizes a 4-phase foliar latent progression timeline ($Day\ 0 \to Day\ 3 \to Day\ 7 \to Day\ 14$) detailing cellular necrosis reduction and chlorophyll recovery.
  3. Synthesizes a physiological biochemical manifold (chlorophyll a/b ratio, stomatal conductance $g_{sw}$, anthocyanin stress index).
  4. Formulates a precision chemical dosage prescription with application instructions.
  5. Discriminator $D(x)$ computes adversarial generator loss, discriminator loss, and an agronomic fidelity score (e.g., 98.2%).
  6. Embeds logged-in agronomist signature and cryptographic verification seal.
- **Destination:** Returned to client for interactive review and formatted for standard browser print/PDF rendering.
- **Output:** Complete, multi-page printable agronomic field dossier.

