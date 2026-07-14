"""
MundaAI — Crop Risk Prediction API
FastAPI backend serving the trained Random Forest classifier.

Run: uvicorn main:app --reload
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import joblib
import pandas as pd
import numpy as np
import os

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="MundaAI API",
    description="AI-powered crop risk prediction for Zimbabwe's smallholder farmers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load model ────────────────────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')

try:
    model      = joblib.load(os.path.join(MODEL_DIR, 'mundaai_model.pkl'))
    le_risk    = joblib.load(os.path.join(MODEL_DIR, 'le_risk.pkl'))
    le_crop    = joblib.load(os.path.join(MODEL_DIR, 'le_crop.pkl'))
    le_province = joblib.load(os.path.join(MODEL_DIR, 'le_province.pkl'))
    print("✅ Model loaded successfully")
except FileNotFoundError:
    print("⚠️  Model files not found. Run the training notebook first.")
    model = None

# ── Features (must match training notebook exactly) ───────────────────────────
FEATURES = [
    'rainfall_mm',
    'ndvi_proxy_0_1',
    'pest_incidents_reported',
    'irrigation_coverage_pct',
    'input_availability_score_0_100',
    'avg_farmgate_price_usd_per_tonne',
    'crop_encoded',
    'province_encoded'
]

# ── Recommendation engine ─────────────────────────────────────────────────────
from recommendations import get_recommendations, get_dominant_factor

# ── Request / Response schemas ────────────────────────────────────────────────
class PredictRequest(BaseModel):
    crop: str = Field(..., example="Groundnuts",
                      description="Crop type: Maize, Groundnuts, Sorghum, Sugar beans, Sunflower, Tomatoes")
    province: str = Field(..., example="Matabeleland North",
                          description="Zimbabwe province")
    rainfall_mm: float = Field(..., ge=0, le=500, example=7.1,
                                description="Rainfall received this month in millimetres")
    ndvi: float = Field(..., ge=0, le=1, example=0.10,
                        description="NDVI vegetation health proxy (0=bare, 1=lush)")
    pest_incidents: int = Field(..., ge=0, le=50, example=10,
                                description="Number of pest incidents observed")
    irrigation_pct: float = Field(..., ge=0, le=100, example=21.4,
                                  description="Irrigation coverage percentage")
    input_availability: float = Field(..., ge=0, le=100, example=41.3,
                                      description="Input availability score (0-100)")
    farmgate_price: float = Field(..., ge=0, example=1308.8,
                                  description="Average farmgate price USD per tonne")

class PredictResponse(BaseModel):
    risk_level: str
    risk_score: float
    confidence: float
    dominant_factor: str
    recommendations: List[str]

# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "product": "MundaAI",
        "description": "AI-powered crop risk prediction for Zimbabwe",
        "version": "1.0.0",
        "endpoints": {
            "predict": "POST /predict",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run the training notebook first."
        )

    # Encode categorical inputs
    try:
        crop_enc = le_crop.transform([request.crop])[0]
    except ValueError:
        valid_crops = list(le_crop.classes_)
        raise HTTPException(
            status_code=400,
            detail=f"Unknown crop '{request.crop}'. Valid crops: {valid_crops}"
        )

    try:
        prov_enc = le_province.transform([request.province])[0]
    except ValueError:
        valid_provinces = list(le_province.classes_)
        raise HTTPException(
            status_code=400,
            detail=f"Unknown province '{request.province}'. Valid provinces: {valid_provinces}"
        )

    # Build feature vector
    features = pd.DataFrame([{
        'rainfall_mm':                      request.rainfall_mm,
        'ndvi_proxy_0_1':                   request.ndvi,
        'pest_incidents_reported':          request.pest_incidents,
        'irrigation_coverage_pct':          request.irrigation_pct,
        'input_availability_score_0_100':   request.input_availability,
        'avg_farmgate_price_usd_per_tonne': request.farmgate_price,
        'crop_encoded':                     crop_enc,
        'province_encoded':                 prov_enc
    }])

    # Predict
    pred_encoded = model.predict(features)[0]
    proba        = model.predict_proba(features)[0]
    risk_level   = le_risk.inverse_transform([pred_encoded])[0]
    confidence   = float(max(proba) * 100)

    # Risk score: use confidence weighted by severity
    severity_weight = {"Low": 0.25, "Medium": 0.60, "High": 0.95}
    risk_score = round(confidence * severity_weight.get(risk_level, 0.5), 1)

    # Dominant factor + recommendations
    dominant_factor = get_dominant_factor(model, FEATURES, request)
    recommendations = get_recommendations(risk_level, dominant_factor, request.crop)

    return PredictResponse(
        risk_level=risk_level,
        risk_score=risk_score,
        confidence=round(confidence, 1),
        dominant_factor=dominant_factor,
        recommendations=recommendations
    )
