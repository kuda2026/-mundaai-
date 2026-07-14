# MundaAI 🌱
### AI-Powered Crop Risk Intelligence for Zimbabwe's Smallholder Farmers

> **"Munda"** — Shona for *farm / field*

[![AI4I Challenge 2026](https://img.shields.io/badge/AI4I-Challenge%202026-green)](https://potraz.gov.zw)
[![Track](https://img.shields.io/badge/Track-Development%20(Track%203)-blue)]()
[![Status](https://img.shields.io/badge/Status-Concept%20MVP-orange)]()

---

## The Problem

Zimbabwe's food insecurity crisis affects **7.7 million people**. Smallholder farmers make planting, pest management, and input decisions without integrated risk intelligence. High-risk situations — converging signals of low rainfall, poor vegetation health, high pest pressure, and limited irrigation — destroy harvests. No current tool alerts farmers **before** it is too late.

Our dataset (360 records, 10 provinces, 6 crops) confirms the pattern:

| Risk level | Avg rainfall | Avg NDVI | Avg pests | Avg irrigation |
|------------|-------------|----------|-----------|----------------|
| Low        | 66.9 mm     | 0.49     | 7.6       | 34.9%          |
| Medium     | 27.9 mm     | 0.32     | 9.6       | 30.6%          |
| **High**   | **16.1 mm** | **0.22** | **12.6**  | **24.3%**      |

Only **4.2%** of records are High-risk — rare, but the most devastating. A standard classifier trained on this imbalance becomes blind to the most dangerous situations.

---

## The Solution

MundaAI gives farmers a **risk label + actionable recommendations** through three channels:

| Channel | Who it serves | How it works |
|---------|--------------|-------------|
| 🌐 **Web app** | Extension officers, connected farmers | Dashboard, risk map, ward reports |
| 💬 **WhatsApp bot** | Farmers with smartphones | Conversational: crop → district → signals → risk + recommendations |
| 📱 **USSD \*384#** | Farmers with basic phones, zero data | 4-step menu → risk label + top action. Zero data cost. |

---

## The AI Core

```
[Farmer inputs] → [CTGAN augmentation] → [Random Forest classifier] → [Recommendation engine] → [Risk label + actions]
```

1. **CTGAN** (Conditional Tabular GAN) — generates synthetic High-risk training samples to fix the 4.2% class imbalance. The model stops being blind to the most dangerous cases.
2. **Random Forest classifier** — trained on 360 real + 85 synthetic Zimbabwean records. Predicts `Low / Medium / High` risk with confidence score.
3. **Recommendation engine** — maps risk level + dominant stress factor to specific, crop-appropriate interventions.

### Sample output — Groundnuts, Lupane, May 2026

```
Risk: HIGH (80.2/100) | Primary driver: Rainfall deficit (7.1mm vs 40mm+ needed)

Recommendations:
1. Stop further planting — soil moisture too low for germination
2. Prioritise irrigation for already-planted rows
3. Apply pesticide within 48 hrs — pest incidents at dangerous threshold
4. Contact extension officer today — government seed aid available in Lupane
5. Consider early harvest of mature pods to salvage yield
```

---

## Repository Structure

```
mundaai/
├── data/
│   ├── 02_agriculture_climate_market_signals.csv   # Training dataset (360 records)
│   └── data_dictionary.md                          # Column descriptions
├── model/
│   ├── 01_mundaai_training.ipynb                   # Full training notebook (run on Colab)
│   ├── mundaai_model.pkl                           # Trained model (generated after running notebook)
│   └── label_encoders.pkl                          # Encoders for categorical features
├── api/
│   ├── main.py                                     # FastAPI prediction endpoint
│   ├── recommendations.py                          # Intervention recommendation logic
│   └── requirements.txt                            # Python dependencies
├── docs/
│   └── architecture.md                             # System architecture description
├── frontend/                                       # React web app (Phase 2)
├── whatsapp/                                       # Twilio webhook (Phase 2)
├── ussd/                                           # Africa's Talking handler (Phase 2)
├── .env.example                                    # Environment variable template (no secrets)
└── README.md
```

---

## Quick Start — Training the Model

1. Open `model/01_mundaai_training.ipynb` in [Google Colab](https://colab.research.google.com)
2. Upload `data/02_agriculture_climate_market_signals.csv` when prompted
3. Run all cells top to bottom (~20–30 minutes)
4. Download `mundaai_model.pkl` from the Colab files panel

---

## Quick Start — Running the API

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

Then POST to `http://localhost:8000/predict`:

```json
{
  "crop": "Groundnuts",
  "province": "Matabeleland North",
  "rainfall_mm": 7.1,
  "ndvi": 0.10,
  "pest_incidents": 10,
  "irrigation_pct": 21.4,
  "input_availability": 41.3,
  "farmgate_price": 1308.8
}
```

Response:
```json
{
  "risk_level": "High",
  "risk_score": 80.2,
  "confidence": 91.5,
  "dominant_factor": "Rainfall deficit",
  "recommendations": [
    "Stop further planting — soil moisture too low for germination",
    "Prioritise irrigation for already-planted rows",
    "Apply pesticide within 48 hrs",
    "Contact extension officer today",
    "Consider early harvest of mature pods"
  ]
}
```

---

## Dataset

- **Source**: Primary research dataset — Zimbabwe agriculture, climate & market signals
- **Size**: 360 records
- **Coverage**: 10 provinces · 6 crops (Maize, Groundnuts, Sorghum, Sugar beans, Sunflower, Tomatoes) · 6 months (Jan–Jun 2026)
- **Features**: Rainfall, NDVI proxy, pest incidents, irrigation coverage, input availability, farmgate price
- **Target**: `risk_level` (Low / Medium / High)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI training | Python, scikit-learn, sdv (CTGAN), pandas, Google Colab |
| API | FastAPI, joblib |
| Web app | React.js, Leaflet.js |
| WhatsApp | Twilio API |
| USSD | Africa's Talking API |
| Hosting | Railway / Render |
| Database | PostgreSQL |

---

## AI4I Challenge 2026

This repository is a submission for the **POTRAZ AI4I Challenge 2026**, Development Track (Track 3).

- **Product**: MundaAI — multi-channel crop risk prediction for Zimbabwe's smallholder farmers
- **Track**: Development (Track 3)
- **Challenge**: AI for Industry (AI4I) Challenge 2026

---

## License

MIT License — open for use, modification, and distribution with attribution.
