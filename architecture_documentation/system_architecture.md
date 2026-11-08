# AgriVision AI — System Architecture & Component Specification

> 🖼️ **High-Resolution Architecture Diagrams:**
> - Layered Architecture (PNG): [`system_architecture.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/system_architecture.png) | (JPG): [`system_architecture.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/system_architecture.jpg)
> - Detailed System Architecture (PNG): [`system_architecture_diagram.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/system_architecture_diagram.png) | (JPG): [`system_architecture_diagram.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/system_architecture_diagram.jpg)
> - Mermaid Source: [`architecture_diagram.mmd`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/architecture_diagram.mmd)

## 1. Architectural Style & Design Principles

AgriVision AI is built upon a **Layered Micro-Modular Architecture (LMMA)** coupled with a **Single-Page Application (SPA) / Decoupled RESTful API Pattern**. The system separates presentation, service orchestration, deterministic decision logic, neural inference, and physical storage.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (SPA)                        │
│          React 19 • Tailwind CSS • Vite • Lucide • Context API         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS / JSON & Multipart
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  API GATEWAY & ROUTING LAYER (ASGI)                    │
│             FastAPI Router • Starlette Middleware • Pydantic           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Python Native Function Dispatch
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC & ORCHESTRATION LAYER                  │
│       Session / Auth Store • Validator • Health • Risk • Recs Engine    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Tensor Data / Feature Vectors
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   AI / ML INFERENCE PIPELINE LAYER                     │
│    EfficientNet CNN • Tabular MLP • HyperLeaf • LSTM • GAN Engines     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ File IO & Memory References
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   STORAGE & PERSISTENCE LAYER (FILESYSTEM)             │
│    Trained Weights (.keras) • Scalers (.pkl) • Uploads • Static Output │
└────────────────────────────────────────────────────────────────────────┘
```

### Key Architectural Principles
1. **Decoupled Client-Server Interaction:** The React user interface communicates with the FastAPI backend strictly via asynchronous REST endpoints over HTTP/HTTPS, enabling independent deployment and maintenance.
2. **Fail-Safe Neural Execution:** Deep learning modules are wrapped in try-catch fallback structures. If optional remote neural services (e.g., Gemini recurrent assistance) fail or lack network access, the system reverts automatically to deterministic local equations without disrupting the user session.
3. **Pre-Inference Validation Gatekeeper:** Unprocessed input images pass through a lightweight OpenCV chromatic verification gate prior to executing multi-megabyte TensorFlow models, preserving server memory and CPU/GPU compute cycles.
4. **Deterministic Agronomic Scoring:** Rather than relying solely on black-box neural predictions for critical decisions, health and risk scores are calculated using transparent, multi-factor agronomic penalty matrices derived from domain expertise.

---

## 2. Detailed Architectural Layer Breakdown

### Layer 1: Presentation Layer (Client Tier)
- **Framework & Runtime:** React 19 SPA running in the client browser, packaged and bundled via Vite.
- **Layout Architecture:**
  - `LandingHero.jsx`: Marketing landing page matching Reference 3 with a 3D isometric perspective glass dashboard, live drone agricultural backdrop, and core capability highlights.
  - `Sidebar.jsx`: Deep-emerald gradient navigation bar matching Reference 2 with rolling hills SVG foliage artwork.
  - `Navbar.jsx`: Global search bar, date pill (`Mon, Oct 27, 2026`), notification center dropdown, and user profile/PFP pill.
  - `DashboardView.jsx`: Core operational screen featuring 4 metric KPI cards with sparkline curves, Farm Overview, Crop Health Trend spline chart, satellite parcel GIS map, Recent Analysis, and Key Insights.
  - `DiseaseView.jsx`: Disease diagnosis scanner matching Reference 1 with camera framing brackets `[ ]`, animated laser scan line, and floating glass diagnosis result card.
  - `YieldView.jsx`: Interactive harvest prediction console with 17 agronomic feature sliders and input fields.
  - `StressView.jsx`: Optical vegetative stress explorer rendering thermal heatmaps, morphological margin overlays, and spectral vegetation indices ($NDI$, $ExG$, $NDVI$, $WBI$).
  - `LSTMTrendView.jsx`: Multi-horizon recurrent sequence explorer displaying 7-day and 14-day vegetative momentum curves, $\pm 1\sigma$ confidence bands, and anomaly warnings.
  - `GANReportView.jsx`: Agri-GAN 2.0 generative dossier generator with latent 4-stage recovery timelines, biochemical stress manifold, and print-ready stylesheet.
  - `SettingsView.jsx`: Profile details, avatar/PFP management, plot parameters, and optional neural engine API key configuration.
  - `AuthModal.jsx`: Multi-method modal supporting Google OAuth simulation, Email/Password login/signup, and SMS Phone OTP verification.
- **State Management:** `AppContext.jsx` using React Context API for global session state (`user`, `lastAnalysis`, `scanHistory`, `notifications`, `currentView`, `geminiApiKey`).
- **Styling & Assets:** Tailwind CSS with custom glassmorphism utilities (`glass-panel`, `glass-card-dark`, custom WebKit scrollbars).

### Layer 2: API Gateway & Routing Layer (Backend Tier)
- **Framework:** FastAPI running on Uvicorn ASGI server on `http://127.0.0.1:8000`.
- **CORS Middleware:** `CORSMiddleware` configured with `allow_origins=["*"]`, `allow_credentials=True`, `allow_methods=["*"]`, and `allow_headers=["*"]`.
- **Static Asset Serving:** Starlette `StaticFiles` mounted at `/outputs` for serving generated visual overlays/heatmaps and at `/assets` for pre-compiled React frontend assets.
- **Single Page Application (SPA) Fallback:** Wildcard route `/{full_path:path}` that intercepts non-API requests and delivers `frontend/dist/index.html`, allowing seamless client-side browser navigation.
- **Request Validation & Data Modeling:** Pydantic schemas validating all incoming JSON bodies (`GoogleAuthRequest`, `EmailAuthRequest`, `PhoneAuthRequest`, `YieldPredictRequest`, `LSTMTrendRequest`, `GANReportRequest`).

### Layer 3: Application Business Logic & Orchestration
- **Authentication Controller:**
  - Manages in-memory user table `USERS_DB` and one-time password dictionary `OTP_STORE`.
  - Maps Google profile tokens, email credentials, or phone numbers to standardized user profiles.
  - Implements demo OTP bypass code (`7729`) for testing.
- **Diagnostic Orchestrator (`detect_leaf_disease`):**
  - Receives uploaded multipart image files and persists them to `outputs/web_uploads/`.
  - Sequentially invokes:
    1. Image Validator (`validate_crop_image`)
    2. Deep Disease Predictor (`predict_disease`)
    3. Spectral Preprocessor & Analyzer (`preprocess_leaf_image`, `analyze_leaf_spectrum`)
    4. Stress Map Visualizer (`generate_stress_visualization`)
    5. Yield Predictor (`predict_crop_yield`)
    6. Health Score Engine (`calculate_health_score`)
    7. Composite Risk Engine (`calculate_risk`)
    8. Forward Forecaster (`generate_forecast`)
    9. Agronomic Recommendation Engine (`generate_recommendations`)
  - Aggregates results into a single standardized diagnostic response payload.
- **Scoring & Risk Engines:**
  - `health_score.py`: Computes 0–100 crop health score based on disease presence, prediction confidence, yield category, pest index, humidity, soil pH, crop species consistency, and optical spectral stress.
  - `risk_engine.py`: Computes weighted composite risk:
    $$\text{Overall Risk} = 0.35 \times \text{Disease} + 0.15 \times \text{Pest} + 0.15 \times \text{Env} + 0.15 \times \text{Yield} + 0.05 \times \text{Consistency} + 0.15 \times \text{Spectral}$$
  - `recommendation_engine.py`: Hierarchical rule-based agronomic advisory system generating targeted chemical, biological, fertigation, and water management protocols.
  - `forecast.py`: Extrapolates 14-day yield and disease risk trends using historical moving average deltas.

### Layer 4: AI / Machine Learning & Inference Pipeline
- **1. Disease Detection Model (`module1/disease_detection/predict.py`):**
  - **Architecture:** EfficientNet Deep Convolutional Neural Network (`models/disease/disease_efficientnet.keras`).
  - **Input Tensor:** $224 \times 224 \times 3$ normalized RGB float array.
  - **Class Dictionary:** 38 classes (`models/disease/class_names.json`) covering 14 crop species and 26 distinct plant pathologies (e.g., Tomato Yellow Leaf Curl, Rice Brown Spot, Apple Scab, Healthy).
  - **Inference Mode:** Softmax probability extraction with top-3 candidate ranking.
- **2. Crop Yield Prediction Model (`module1/yield_prediction/predict.py`):**
  - **Architecture:** Multi-Layer Perceptron (`models/module1/crop_yield_mlp.keras`).
  - **Preprocessing:** Scikit-learn column transformer (`preprocessor.pkl`) applying OneHotEncoding to 7 categorical features and StandardScaler to 10 numerical features.
  - **Output:** Scalar float representing metric tons per hectare ($t/ha$).
- **3. Optical & Spectral Stress Analyzer (`intelligence/spectral/`):**
  - **Algorithms:** OpenCV Excess Green ($ExG$), Normalized Difference Greenness ($NDI$), and HSV thresholding.
  - **Artifact Generation:** Generates Jet colormap thermal heatmaps (`*_heatmap.jpg`) and green boundary morphological overlays (`*_overlay.jpg`).
  - **Deep Hyperspectral Model:** HyperLeaf 204-band spectral regression network (`models/spectral/hyperleaf_spectral.keras`) with feature and target scalers (`.pkl`).
- **4. Recurrent LSTM Trend Forecaster (`intelligence/forecasting/lstm_trend_engine.py`):**
  - **Architecture:** Multi-Horizon Recurrent Sequence Forecaster.
  - **Engine Logic:** Models cell state velocity, vegetative momentum, and Gaussian volatility envelopes.
  - **Gemini REST Integration:** Leverages Gemini API via HTTP POST with strict JSON schema to simulate deep LSTM multi-step state projections, with seamless fallback to native recurrent math.
- **5. Generative Adversarial Report Synthesizer (`intelligence/generative/gan_report_engine.py`):**
  - **Architecture:** Conditional Generative Adversarial Network ($c$-GAN) formulation.
  - **Generator $G(z \mid c)$:** Synthesizes multi-page agronomic diagnostic dossiers, latent 4-stage foliar regeneration timelines ($Day\ 0 \to 14$), and precision intervention formulations.
  - **Discriminator $D(x)$:** Evaluates biological plausibility, outputting a discriminator fidelity score (e.g., 98.2%) and generator loss metrics.

### Layer 5: Data Storage & Persistence Tier
- **In-Memory Volatile Storage:** Python dictionaries maintaining active user accounts (`USERS_DB`) and temporary SMS verification codes (`OTP_STORE`).
- **Filesystem Storage:**
  - `outputs/web_uploads/`: Staging directory for raw user-uploaded leaf photographs.
  - `outputs/spectral/`: Generated visual assets including heatmaps, boundary masks, and morphological overlays.
  - `models/`: Trained neural network binaries (`.keras`) and Scikit-learn transformers (`.pkl`).
- **Client-Side Persistence:** Browser `localStorage` storing user session JSON (`agrivision_user`) and optional acceleration API keys (`agrivision_gemini_key`).

---

## 3. Component Responsibility Table

| Component | Technology | Responsibility | Input | Output |
| :--- | :--- | :--- | :--- | :--- |
| **Vite / React Client** | React 19, Tailwind CSS | Manages user interface, views, forms, client routing, and state | User mouse/keyboard inputs, file selections, camera feed | Rendered DOM elements, HTTP requests to API Gateway |
| **App Context Provider** | React Context API | Stores global session state (user profile, scans, notifications, API key) | Authentication data, API scan responses | React state props consumed across all UI components |
| **API Gateway / Router** | FastAPI, Starlette | Routes incoming HTTP requests, handles CORS, validates payloads, serves SPA | HTTP REST requests (GET, POST, PUT) | HTTP JSON responses, static binary files, SPA HTML |
| **Auth Controller** | Python, Pydantic | Authenticates Google, Email, and Phone OTP sessions; manages users | `GoogleAuthRequest`, `EmailAuthRequest`, `PhoneAuthRequest` | JWT token string, structured user profile dictionary |
| **Image Validator** | OpenCV (cv2), NumPy | Pre-inference quality verification: resolution check, HSV green vegetation ratio | Raw leaf image file path on disk | Validation dictionary (`valid: bool`, `green_ratio`, `reason`) |
| **Disease Detection Pipeline** | TensorFlow 2.10, Keras | Classifies crop leaf disease and identifies botanical crop species | Preprocessed leaf image ($224 \times 224 \times 3$ tensor) | Prediction dictionary (`crop`, `disease`, `confidence`, top-3) |
| **Spectral Visualizer** | OpenCV (cv2), NumPy | Computes chromatic vegetative indices ($ExG$, $NDI$) and generates overlays | Leaf image file path on disk | Generated heatmap and morphological overlay JPEG images on disk |
| **Yield Prediction Pipeline** | Keras, Scikit-learn, Joblib | Computes expected crop yield in metric tons per hectare ($t/ha$) | 17-feature agronomic vector (soil, weather, inputs) | Float predicted yield ($t/ha$) and categorical yield rating |
| **Crop Health Scoring Engine** | Python Math / Logic | Fuses disease, yield, pest, weather, pH, and stress into a 0–100 health score | Disease confidence, yield category, pest index, pH, stress | Health score float (0–100) and qualitative status string |
| **Farm Risk Engine** | Python Math / Logic | Calculates composite weighted farm risk across six agricultural vectors | Disease risk, pest index, humidity, yield, spectral stress | Overall risk score float (0–100) and risk level tier |
| **Recommendation Engine** | Python Rule Matrix | Formulates priority-ranked chemical, biological, and cultural prescriptions | Diagnosed disease, crop, health score, soil pH, humidity | Prioritized list of actionable agronomic instructions |
| **LSTM Trend Forecaster** | Python, Gemini API REST | Models multi-horizon temporal trajectories and flags time-series anomalies | Baseline health, yield, risk, soil nitrogen, horizon days | 7-day and 14-day projection array with confidence bands |
| **GAN Report Synthesizer** | Python, Generative Logic | Generates multi-stage latent foliar recovery timelines and expert dossiers | Diagnosed field parameters, farmer metadata, stress scores | Comprehensive GAN dossier dictionary and printable report |
| **Local Filesystem Store** | Windows NTFS / Disk | Persists neural model weights, scalers, uploads, and visual artifacts | Binary write streams from models, uploads, OpenCV | Stored files (`.keras`, `.pkl`, `.jpg`, `.png`, `.json`) |

---

## 4. Cross-Cutting Concerns & Security Mechanisms

### 4.1 Authentication & Session Management
- **Google Authentication:** Handles Google identity credentials or email claims, automatically populating verified names and profile pictures.
- **Email Registration:** Validates email format, checks for collisions against `USERS_DB`, and links chosen avatars.
- **Phone OTP Verification:** Formats international mobile numbers, issues verification codes via `OTP_STORE`, and validates entries using a standardized test code (`7729`).
- **Token Dispatch:** Returns simulated session tokens (`jwt-agri-{uuid}`) for authenticated client requests.

### 4.2 Data Validation & Pre-Inference Guards
- **Schema Validation:** Strict Pydantic models validate incoming data types, ranges, and defaults for all JSON payloads.
- **Binary File Inspection:** Image uploads are verified for existence, decoded via OpenCV, checked for minimum dimensions ($100 \times 100$ pixels), and evaluated for vegetation chromatic presence ($\text{green ratio} \ge 1.0\%$) to block non-leaf uploads from reaching the neural networks.

### 4.3 Error Handling & Fault Tolerance
- **HTTP Exception Mapping:** Catches system errors and transforms them into standardized `HTTPException(status_code=500, detail=str(e))` JSON responses.
- **Graceful Network Degradation:** In `lstm_trend_engine.py`, network timeouts or invalid Gemini keys trigger an automatic fallback to local recurrent sequence simulation without breaking the UI.
- **Missing File Protection:** All model loader utilities check file existence before calling TensorFlow `load_model`, raising descriptive `FileNotFoundError` exceptions if paths are invalid.

### 4.4 Communication Protocols
- **Client to Backend:** Synchronous HTTP/1.1 REST calls over JSON and multipart/form-data.
- **Backend to Gemini API:** Synchronous HTTPS POST requests over TLS 1.3 with application/json payloads and a 12-second timeout window.
- **Backend to Filesystem:** Synchronous native Windows file IO for reading model weights and writing image artifacts.

