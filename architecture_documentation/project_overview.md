# AgriVision AI — Project Overview & Technical Specification

> 🖼️ **High-Resolution Diagram Assets:**
> - Poster Image (PNG): [`project_overview.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/project_overview.png) (300 DPI)
> - Poster Image (JPG): [`project_overview.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/project_overview.jpg) (300 DPI)

## 1. Project Introduction

### 1.1 Project Name
**AgriVision AI** — Unified Crop Intelligence & Precision Agriculture Platform.

### 1.2 Domain and Category
- **Domain:** Precision Agriculture, Digital Agronomy, AgriTech, Smart Farming.
- **Category:** Full-Stack Intelligent Decision Support System (DSS) combining Computer Vision, Deep Learning, Recurrent Neural Time-Series Forecasting, and Generative Adversarial Synthesis.

### 1.3 Brief Introduction
AgriVision AI is an end-to-end intelligent agricultural diagnosis and farm management platform. It transforms raw visual and environmental field data into real-time agronomic insights. By consolidating foliar disease detection, multi-spectral vegetative stress mapping, tabular crop yield prediction, temporal health trend forecasting, and generative adversarial diagnostic reporting into a single interface, AgriVision AI equips farmers, agronomists, and agricultural enterprises with actionable, data-driven interventions.

### 1.4 Problem Statement
Modern agriculture faces severe threats from unmonitored crop pathogens, delayed disease diagnosis, unpredictable weather volatility, sub-optimal fertilizer and pesticide application, and lack of localized predictive intelligence:
1. **Late Pathogen Identification:** Visual foliar symptoms are often identified manually after irreversible canopy damage and sporulation have occurred, reducing crop yield by 20% to 40%.
2. **Fragmented Diagnostics:** Soil health, meteorological readings, visual symptoms, and yield forecasting are traditionally siloed across disconnected tools, preventing unified risk analysis.
3. **Subjective & Non-Standardized Recommendations:** Smallholder and commercial growers often lack immediate access to certified agronomists, leading to indiscriminate chemical spraying, soil degradation, and high financial losses.
4. **Lack of Forward-Looking Trajectory Projections:** Existing tools provide point-in-time detection without projecting how foliar disease and vegetative health will evolve over 7-to-14-day horizons.

### 1.5 Why This Project is Needed
AgriVision AI bridges the gap between state-of-the-art deep learning research and practical, daily farm management. It provides:
- **Instant Optical Disease Diagnosis:** Sub-second identification of foliar crop diseases from mobile camera snapshots or drone imagery.
- **Physiological & Multi-Spectral Stress Mapping:** Synthesis of vegetative index overlays (Excess Green Index, Normalized Green Index, HSV chromatic segmentation) to pinpoint early cellular chlorosis.
- **Multi-Factor Harvest Yield Projection:** Tabular Neural Network (MLP) calculating metric tons per hectare based on soil chemistry (N-P-K, pH), meteorological variables, and agronomic management practices.
- **Multi-Horizon Recurrent Temporal Forecasting:** Bi-directional sequence modeling simulating future vegetative momentum, biomass accretion, and volatility envelopes.
- **Generative Adversarial Synthesis (GAN):** Automated creation of certified agronomic dossiers detailing progressive cellular recovery timelines and calibrated chemical/biological treatments.

---

## 2. Project Objectives

1. **High-Accuracy Foliar Pathogen Classification:** Deploy a deep convolutional neural network (EfficientNet architecture) capable of classifying healthy foliage and diverse disease classes across major crop types (Rice, Tomato, Apple, Potato, Corn, Grape, Pepper, Peach, Cherry).
2. **Automated Optical Image Quality & Vegetation Validation:** Reject non-leaf or corrupted uploads through real-time HSV chromatic filtering, luminance distribution checks, and green vegetation ratio thresholding before executing compute-heavy neural models.
3. **Holistic Agronomic Health & Risk Computation:** Formulate deterministic, multi-factor scoring engines that fuse disease confidence, yield potential, pest pressure, environmental humidity, soil pH, and optical stress into standardized indices (0–100 scale).
4. **Temporal Recurrent Dynamics:** Provide 7-day and 14-day forward health trajectories using recurrent neural cell dynamics with confidence envelopes and anomaly alerts.
5. **Generative Diagnostic Dossier Creation:** Implement a conditional GAN-inspired generative engine that projects latent foliar recovery stages ($Day\ 0 \to Day\ 3 \to Day\ 7 \to Day\ 14$) and formulates multi-tiered agronomic prescriptions validated by a discriminator fidelity metric.
6. **Multi-Channel Identity & Authentication:** Deliver an enterprise-grade authentication system supporting Google OAuth profiles, Email/Password credentialing, and SMS Phone OTP verification with custom farmer avatar/PFP synchronization.
7. **Responsive High-Performance UI:** Provide a responsive SaaS dashboard adhering to modern precision agriculture design systems (matching dark-emerald glassmorphism layouts, live sparklines, interactive GIS field maps, and print-ready dossiers).

---

## 3. Key Features

### 3.1 Intelligent Disease Detection & Camera Scanner
- **Multi-Source Ingestion:** Accepts direct mobile/webcam frame captures, local file uploads (JPEG, PNG, WebP), or instant one-click benchmark leaf presets.
- **Visual Target Framing:** Viewport interface with target brackets `[ ]`, animated laser scan indicators, and real-time bounding box annotations.
- **Multi-Class Output:** Classifies disease identity, botanical crop species, confidence percentage, and secondary prediction candidates.
- **Automatic Crop Consistency Verification:** Compares the user-declared crop against the deep learning-predicted botanical class, penalizing discrepancies in overall health scoring.
- **Validated Classification Performance:** Achieves **94.85% overall validation accuracy** across 14,059 unseen foliar samples (**95.19% Weighted F1-Score**, **95.63% Weighted Precision**). High-resolution visual benchmarks available in [`confusion_matrix.png`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/confusion_matrix.png) and [`confusion_matrix.jpg`](file:///c:/Users/utsha/Downloads/Agrovision/Agrovision/AgriVisionAI/architecture_documentation/confusion_matrix.jpg).

### 3.2 Hyperspectral & Optical Stress Analysis
- **Chromatic Index Computation:** Calculates the Excess Green Index ($ExG = 2g - r - b$) and Normalized Difference Greenness Index ($NDI = \frac{g - r}{g + r}$).
- **Foliar Heatmap Generation:** Converts optical reflection gradients into thermal-style stress heatmaps using OpenCV color mapping (`COLORMAP_JET`).
- **Pathogen Margin Morphological Overlay:** Outlines chlorotic halos and necrotic lesions over the original RGB leaf image and saves the artifacts for visual inspection.
- **Spectral Stress Rating:** Quantifies cellular chlorosis into a standardized 0–100 stress score incorporated into holistic farm health calculations.

### 3.3 Neural MLP Crop Yield Prediction
- **17-Feature Agronomic Vector:** Ingests numerical inputs (rainfall in mm, average temperature in °C, humidity percentage, soil pH, Nitrogen kg/ha, Phosphorus kg/ha, Potassium kg/ha, irrigation volume in mm, days since harvest, pest index) and categorical features (soil type, crop variety, fertilization status, weather zone, seed quality, irrigation method, season).
- **Preprocessed Scaling:** Employs scikit-learn transformers (`preprocessor.pkl`) for categorical One-Hot Encoding and numerical Standard Scaling.
- **Multi-Layer Perceptron:** Dense neural network (`crop_yield_mlp.keras`) executing forward inference to predict expected crop yield in metric tons per hectare ($t/ha$).

### 3.4 Deep Recurrent LSTM Multi-Horizon Trend Forecaster
- **Sequential Recurrent Dynamic Modeling:** Ingests temporal sequences of canopy vigor, soil nutrient availability, and ambient risk.
- **Multi-Horizon Projections:** Projects future crop health trajectories over 7-day and 14-day intervals with upper/lower $\pm 1\sigma$ confidence bands.
- **Cell State Velocity & Anomaly Detection:** Calculates rate-of-change momentum and flags micro-climate variances (e.g., Vapor Pressure Deficit deviations, nitrogen assimilation crashes).
- **Dual-Mode Engine:** Powered by a Gemini-driven temporal sequence prompt protocol behind the scenes when configured with an API key, backed by deterministic analytical recurrent equations when offline.

### 3.5 Agri-GAN 2.0 Generative Report Synthesizer
- **Conditional Adversarial Dossier Generation:** Ingests field diagnostics ($c$) to synthesize structured agronomic reports via generator $G(z \mid c)$.
- **Latent Foliar Regeneration Timeline:** Generates a 4-phase biological timeline ($Day\ 0\text{ Baseline} \to Day\ 3\text{ Inactivation} \to Day\ 7\text{ Regeneration} \to Day\ 14\text{ Restoration}$) detailing cellular necrosis reduction and chlorophyll recovery.
- **Biochemical Stress Manifold:** Synthesizes physiological indicators including Chlorophyll a/b ratios, Stomatal Conductance ($g_{sw}$), and Anthocyanin stress markers.
- **Discriminator Validation:** Computes discriminator fidelity scores (e.g., 98.2%) and generator loss metrics to certify agronomic coherence.
- **Print & PDF Export:** One-click generation of field-ready agronomic dossiers complete with agronomist credentials and cryptographic verification stamps.

### 3.6 Multi-Channel Authentication & Profile Customization
- **Three Authentication Vectors:**
  1. *Google Account:* Instant profile synchronization importing Google name, verified email, and profile avatar.
  2. *Email & Password:* Standard credential registration with custom name and avatar assignment.
  3. *Phone & OTP:* SMS verification flow with automatic mobile identifier formatting and demo code support (`7729`).
- **Dynamic Avatar/PFP Synchronization:** Profile pictures are displayed across the top navigation bar, the dashboard welcome banner (*"Welcome Back, [Name]! 👋"*), account settings, and generated reports.

### 3.7 Interactive Precision Agriculture Dashboard
- **Top KPI Cards:** Four summary cards with colored sparklines (*Crop Health %*, *Predicted Yield t/ha*, *Composite Risk Level*, *Current Meteorological Weather*).
- **Farm Overview:** Summary card detailing target crop species, season, N-P-K soil ratio, and GPS plot location.
- **Interactive Health Trend:** Historical 7-day SVG spline chart with interactive data nodes.
- **Satellite Field GIS Parcel:** Interactive field map with boundary polygon highlighting, risk category legends (Healthy, At Risk, Diseased), and zoom controls.
- **Key Insights & Advisory:** Real-time agronomic insights highlighting yield potential deltas, disease risk alerts, and direct navigation to treatment plans.

---

## 4. Technology Stack

### 4.1 Frontend Layer
| Technology / Package | Version | Purpose in Codebase |
| :--- | :--- | :--- |
| **React** | 19.2.0 | Core UI component library and virtual DOM rendering |
| **Vite** | 8.3.5 | Build tool, development server, and optimized asset bundler |
| **Tailwind CSS** | 3.4.17 | Utility-first styling, glassmorphism design system, responsive grids |
| **PostCSS & Autoprefixer** | 8.5.8 / 10.4.27 | CSS transformation and cross-browser vendor prefixing |
| **Lucide React** | 1.16.0 | Vector iconography for agricultural and UI elements |
| **React Context API** | Native | Centralized global application state (`AppContext.jsx`) |

### 4.2 Backend Layer
| Technology / Package | Version | Purpose in Codebase |
| :--- | :--- | :--- |
| **Python** | 3.10.11 | Primary backend runtime environment |
| **FastAPI** | 0.141.1 | Asynchronous RESTful API framework with OpenAPI documentation |
| **Uvicorn** | 0.52.4 | ASGI web server hosting the FastAPI application |
| **Starlette** | 1.6.0 | Underlying ASGI toolkit providing static file mounts and routing |
| **Pydantic** | 2.13.4 | Request payload parsing, schema validation, and data serialization |
| **Python-Multipart** | 0.0.32 | Multipart/form-data parser for image and file uploads |

### 4.3 AI / Machine Learning & Computer Vision
| Technology / Package | Version | Purpose in Codebase |
| :--- | :--- | :--- |
| **TensorFlow** | 2.10.0 | Deep learning framework for loading and executing trained Keras models |
| **Keras** | 2.10.0 | High-level neural network API (`load_model`, sequential/functional inference) |
| **OpenCV (cv2)** | 5.0.0.93 | Computer vision algorithms: HSV filtering, chromatic indices, colormaps |
| **Scikit-learn** | 1.7.2 | Preprocessing pipelines (`OneHotEncoder`, `StandardScaler`) for MLP features |
| **Joblib** | 1.5.3 | Serialized model and transformer loading (`preprocessor.pkl`, scalers) |
| **NumPy** | 1.26.4 | Numerical matrix manipulation, tensor math, percentile calculations |
| **Pandas** | 2.3.3 | Dataframe structures for tabular yield prediction feature vectors |
| **Pillow (PIL)** | 12.3.0 | Image file decoding, format conversions, and canvas rendering |
| **Google Generative AI SDK**| 0.8.6 | REST integration for Gemini-assisted LSTM sequence forecasting |

### 4.4 Data Storage & Artifact Systems
| Storage Mechanism | Type | Purpose in Codebase |
| :--- | :--- | :--- |
| **In-Memory Store (`USERS_DB`)** | Memory Dict | Session and registered user records keyed by email/phone |
| **In-Memory Store (`OTP_STORE`)** | Memory Dict | Temporary verification codes for phone authentication |
| **Local File System (`outputs/web_uploads/`)** | Disk Storage | User-uploaded crop leaf images for model inference |
| **Local File System (`outputs/spectral/`)** | Disk Storage | Generated stress heatmaps, binary masks, and visual overlays |
| **Local File System (`models/`)** | Disk Storage | Serialized Keras neural network weights and joblib scalers |
| **Browser LocalStorage** | Client Storage | User profile persistence (`agrivision_user`) and API keys |

### 4.5 Development & Packaging Infrastructure
| Tool | Purpose in Codebase |
| :--- | :--- |
| **Node.js (v24.19.0) & npm (11.17.0)** | Node runtime and package management for frontend compilation |
| **Windows PowerShell / Batch Scripts** | Execution scripts (`run_app.bat`, `start_dev.bat`) for automated platform launch |

---

## 5. System Modules

```
AgriVisionAI/
├── api_server.py                       # FastAPI entrypoint, routes, middleware, static mounts
├── dashboard.py                        # Legacy Tkinter desktop interface
├── run_app.bat                         # Automated single-click launcher (Backend + Browser)
├── start_dev.bat                       # Full-stack dev launcher (FastAPI + Vite dev server)
├── frontend/                           # Modern React 19 web application
│   ├── src/
│   │   ├── App.jsx                     # Top-level view router and master layout
│   │   ├── main.jsx                    # React root mounter with AppProvider
│   │   ├── index.css                   # Tailwind base, utilities, and animations
│   │   ├── context/
│   │   │   └── AppContext.jsx          # Global context (auth, active scans, history, API key)
│   │   └── components/
│   │       ├── Navbar.jsx              # Search, date pill, notification dropdown, user PFP menu
│   │       ├── Sidebar.jsx             # Emerald sidebar navigation with foliage background
│   │       ├── AuthModal.jsx           # Multi-method authentication (Google, Email, Phone/OTP)
│   │       ├── LandingHero.jsx         # Reference 3 landing hero with 3D floating glass dashboard
│   │       ├── DashboardView.jsx       # Reference 2 main dashboard with KPI cards and GIS map
│   │       ├── DiseaseView.jsx         # Reference 1 disease detection with camera brackets [ ]
│   │       ├── LSTMTrendView.jsx       # Deep recurrent LSTM temporal trend forecaster
│   │       ├── GANReportView.jsx       # Agri-GAN 2.0 generative adversarial diagnostic dossier
│   │       ├── YieldView.jsx           # Tabular MLP crop harvest yield prediction calculator
│   │       ├── StressView.jsx          # Hyperspectral foliar stress and optical index mapper
│   │       ├── AdvisoryView.jsx        # Expert agronomic recommendations and action protocols
│   │       └── SettingsView.jsx        # Profile, PFP/avatar management, and farm parameters
├── module1/                            # Core Deep Learning Modules
│   ├── disease_detection/
│   │   └── predict.py                  # EfficientNet leaf disease prediction pipeline
│   └── yield_prediction/
│       └── predict.py                  # Tabular MLP crop yield prediction pipeline
├── intelligence/                       # Integrated Agronomic Intelligence Engines
│   ├── image_validation/
│   │   └── validator.py                # Pre-inference image validity & vegetation ratio check
│   ├── health/
│   │   └── health_score.py             # Multi-factor crop health score calculation engine
│   ├── risk/
│   │   └── risk_engine.py              # Composite weighted farm risk assessment engine
│   ├── forecast/
│   │   └── forecast.py                 # Multi-day moving trend extrapolation engine
│   ├── recommendations/
│   │   └── recommendation_engine.py    # Hierarchical agronomic treatment prescription engine
│   ├── spectral/                       # Hyperspectral analysis package
│   │   ├── analyzer.py                 # Optical feature extractor
│   │   ├── preprocessing.py            # Spectral tensor preparation
│   │   ├── visualizer.py               # ExG, NDI, and thermal heatmap overlay generator
│   │   └── model/predict.py            # HyperLeaf 204-band model predictor
│   ├── forecasting/
│   │   └── lstm_trend_engine.py        # Gemini-assisted recurrent LSTM temporal trend engine
│   └── generative/
│       └── gan_report_engine.py        # Conditional GAN report synthesizer and discriminator
├── models/                             # Trained Neural Weights & Serialized Artifacts
│   ├── disease/
│   │   ├── disease_efficientnet.keras  # Trained convolutional neural network for disease
│   │   └── class_names.json            # 38 plant disease class label dictionary
│   ├── module1/
│   │   ├── crop_yield_mlp.keras        # Trained multi-layer perceptron for yield prediction
│   │   └── preprocessor.pkl            # Scikit-learn tabular column transformer
│   ├── forecasting/
│   │   ├── crop_yield_lstm.keras       # Trained LSTM recurrent sequence model
│   │   └── lstm_scaler.pkl             # Serialized MinMaxScaler for LSTM inputs
│   └── spectral/
│       ├── hyperleaf_spectral.keras    # Trained hyperspectral stress regression model
│       ├── hyperleaf_feature_scaler.pkl# Feature scaling transformer
│       └── hyperleaf_target_scaler.pkl # Target scaling transformer
└── outputs/                            # Dynamic Output Generation Directory
    ├── web_uploads/                    # Storage for uploaded leaf images
    └── spectral/                       # Output artifacts (heatmaps, overlays, masks)
```

---

## 6. Complete Working Process

The lifecycle of an end-to-end user workflow proceeds as follows:

```
[User Interaction]
       │
       ▼
1. Authentication & Context Initialization
   - User signs in via Google OAuth, Email/Password, or Phone OTP.
   - Profile picture (PFP), name, and farm location are synced into global state (`AppContext`).
       │
       ▼
2. Diagnostic Image Acquisition
   - User uploads a leaf image or captures a live frame in the Disease Detection view (`/disease`).
   - The React client streams the binary file via multipart/form-data to `POST /api/disease/detect`.
       │
       ▼
3. Pre-Inference Validation
   - `validator.py` checks dimensions ($\ge 100 \times 100$), calculates HSV green ratio ($[20, 30, 20]$ to $[100, 255, 255]$),
     and verifies vegetation presence. If invalid, processing halts with a descriptive error.
       │
       ▼
4. Multi-Model Inference Pipeline
   ├── A. Disease Detection: `predict.py` resizes image to $224 \times 224$ and executes `disease_efficientnet.keras`.
   ├── B. Spectral Stress Analysis: `visualizer.py` computes $ExG$, $NDI$, and HSV masks, exporting heatmap and overlay images.
   └── C. Harvest Yield Prediction: `predict.py` executes `crop_yield_mlp.keras` with soil, weather, and management inputs.
       │
       ▼
5. Decision Support & Scoring Synthesis
   ├── A. Crop Health Score: `health_score.py` calculates 0–100 score with calibrated disease, yield, and stress penalties.
   ├── B. Composite Risk Level: `risk_engine.py` computes weighted risk across disease (35%), pest (15%), weather (15%), yield (15%), consistency (5%), and stress (15%).
   ├── C. Actionable Recommendations: `recommendation_engine.py` generates priority-ranked treatment protocols.
   └── D. 14-Day Baseline Forecast: `forecast.py` projects projected yield and risk trends.
       │
       ▼
6. Temporal Recurrent LSTM Forecasting
   - User navigates to `/forecast`. `lstm_trend_engine.py` models temporal sequences over a 14-day horizon.
   - Calculates hidden cell velocity, confidence intervals, and flags anomalies (e.g., VPD, nutrient crashes).
       │
       ▼
7. Generative GAN Dossier Creation
   - User requests a comprehensive report (`/reports`). `gan_report_engine.py` executes conditional adversarial synthesis.
   - Generates foliar recovery stages ($Day\ 0 \to 14$), biochemical markers, and treatment matrices with a 98.2% discriminator fidelity score.
   - User reviews the report on-screen or prints/exports it as an official PDF dossier.
```

---

## 7. Expected Outcomes

- **Reduction in Crop Damage:** Rapid identification of foliar pathogens allows farmers to treat infections within 24 to 48 hours of symptom appearance, preventing widespread epidemic spread.
- **Resource Optimization:** Precise, disease-specific fungicide and fertilizer prescriptions reduce chemical runoff, minimize soil toxicity, and cut input costs by up to 25%.
- **Accurate Yield Forecasting:** Multi-factor neural yield predictions assist growers and agricultural cooperatives in financial planning, forward contracting, and supply chain logistics.
- **Democratized Agronomic Expertise:** Smallholder farmers gain instant access to expert-level diagnostic intelligence without waiting for on-site agronomist visits.
- **Archival Farm Intelligence:** Generates permanent, verifiable diagnostic records (GAN dossiers) documenting historical field health, pathogen occurrences, and mitigation efficacy over consecutive growing seasons.

