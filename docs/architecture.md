# MundaAI — System Architecture

## Overview

```
Farmer (any device)
        │
        ├── Web App (React)      ─┐
        ├── WhatsApp Bot (Twilio) ├──→ FastAPI  →  Random Forest Model  →  Risk Label
        └── USSD *384# (AT)      ─┘   /predict      + CTGAN augmented       + Recommendations
                                        
                                       PostgreSQL (anonymous logs)
```

## AI Pipeline

```
02_agriculture_climate_market_signals.csv (360 records)
        │
        ▼
[Feature Engineering]
  - Encode: crop, province → integers
  - Features: rainfall, NDVI, pests, irrigation, input_avail, price, crop_enc, province_enc
        │
        ▼
[CTGAN Augmentation]
  - Problem: Only 15/360 (4.2%) are High-risk
  - CTGAN learns joint distribution of High-risk signal values
  - Generates 85 synthetic High-risk records
  - Result: balanced training set (172 Low / 173 Medium / 100 High)
        │
        ▼
[Random Forest Classifier]
  - n_estimators=200, class_weight='balanced'
  - Trained on real + synthetic data
  - Outputs: risk_level + class probabilities
        │
        ▼
[Recommendation Engine]
  - Maps: risk_level + dominant_factor + crop → ranked actions
  - Rule-based (human-curated for agricultural accuracy)
        │
        ▼
[API Response]
  {risk_level, risk_score, confidence, dominant_factor, recommendations[]}
```

## Three Access Channels

| Channel    | Entry point | Parser               | Stack                     | Connectivity |
|------------|-------------|----------------------|---------------------------|-------------|
| Web        | React form  | Direct API call      | React + Leaflet + FastAPI | Requires internet |
| WhatsApp   | Chat message| NLP intent parser    | Twilio webhook + Flask    | Requires WhatsApp |
| USSD       | *384#       | Menu selections      | Africa's Talking + Flask  | Zero data needed |

All three channels hit the same `/predict` FastAPI endpoint. The only difference is how inputs are collected and how the response is formatted.

## Data Flow — USSD Example

```
Farmer dials *384#
    ↓
Africa's Talking sends POST to /ussd webhook
    ↓
Menu: "Select crop: 1=Maize 2=Groundnuts 3=Sorghum 4=Sugar beans 5=Sunflower 6=Tomatoes"
    ↓
Menu: "Select province: 1=Mashonaland Central 2=Mashonaland East ... 10=Matabeleland South"
    ↓
Menu: "How much rain this month? 1=<10mm 2=10-30mm 3=30-60mm 4=>60mm"
    ↓
Menu: "Pest level? 1=None 2=Some 3=Many 4=Severe"
    ↓
POST /predict with encoded values
    ↓
Response formatted to 160 chars:
"RISK: HIGH. Main cause: Rainfall deficit.
Action: Stop planting. Irrigate existing crop. Contact extension officer. Dial *384*2# for more."
```

## Security

- No PII collected at any channel (USSD sessions are stateless; WhatsApp stores only crop/district/signal inputs)
- API keys stored in environment variables only — never in code
- Role-based access on web app: farmer / extension officer / admin / MoA
- All predictions labelled as "risk indicators" — not directives
