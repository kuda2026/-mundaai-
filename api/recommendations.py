"""
MundaAI — Recommendation Engine
Maps risk level + dominant factor + crop → specific actionable interventions.
"""

FEATURES = [
    'rainfall_mm', 'ndvi_proxy_0_1', 'pest_incidents_reported',
    'irrigation_coverage_pct', 'input_availability_score_0_100',
    'avg_farmgate_price_usd_per_tonne', 'crop_encoded', 'province_encoded'
]

FACTOR_NAMES = {
    'rainfall_mm':                      'Rainfall deficit',
    'ndvi_proxy_0_1':                   'Poor vegetation health (low NDVI)',
    'pest_incidents_reported':          'High pest pressure',
    'irrigation_coverage_pct':          'Limited irrigation coverage',
    'input_availability_score_0_100':   'Low input availability',
    'avg_farmgate_price_usd_per_tonne': 'Unfavourable market price',
    'crop_encoded':                     'Crop vulnerability',
    'province_encoded':                 'Regional risk factors',
}


def get_dominant_factor(model, feature_names, request) -> str:
    """Return the human-readable name of the most important feature."""
    importances = dict(zip(feature_names, model.feature_importances_))
    # Only rank the interpretable field-level features
    interpretable = [f for f in feature_names if f in FACTOR_NAMES]
    top = max(interpretable, key=lambda f: importances.get(f, 0))
    return FACTOR_NAMES.get(top, top)


# ── Crop-specific recommendations by risk level & dominant factor ─────────────

RECS = {
    "High": {
        "Rainfall deficit": [
            "Stop further planting immediately — soil moisture is too low for germination",
            "Prioritise irrigation for already-planted rows; even partial watering helps",
            "Apply drought-tolerant mulch to retain existing soil moisture",
            "Contact your district extension officer today — emergency seed aid may be available",
            "Consider early harvesting of any mature crop to salvage yield",
            "Document losses for government crop insurance or relief programme eligibility",
        ],
        "High pest pressure": [
            "Apply recommended pesticide within 48 hours — pest levels are at a dangerous threshold",
            "Scout all fields urgently and map affected areas",
            "Notify your extension officer — district-level spraying programmes may be activated",
            "Do not plant new areas until pest population is under control",
            "Use pheromone traps or biological controls as supplementary measures",
            "Remove and destroy heavily infested plants to limit spread",
        ],
        "Poor vegetation health (low NDVI)": [
            "Assess whether poor NDVI is caused by drought, pest damage, or disease",
            "Apply foliar fertiliser if nutrient deficiency is suspected",
            "Increase irrigation frequency if water is available",
            "Contact extension officer for soil test and crop health assessment",
            "Avoid applying additional inputs until the root cause is identified",
        ],
        "Limited irrigation coverage": [
            "Prioritise irrigation for the highest-value or most mature crop areas",
            "Check borehole and pump functionality — ensure maximum water output",
            "Consider furrow irrigation to reduce water use while maintaining coverage",
            "Contact district water authority about emergency water access",
            "As a last resort, focus resources on the smallest area with the highest yield potential",
        ],
        "Low input availability": [
            "Source inputs from the nearest town agro-dealer immediately — do not wait",
            "Check with your extension officer about government input subsidy programmes",
            "Prioritise pesticide over fertiliser if pest pressure is elevated",
            "Share inputs with neighbouring farmers to reduce individual cost",
            "Consider delaying planting if inputs cannot be sourced within one week",
        ],
        "default": [
            "This is a HIGH RISK situation — take immediate action",
            "Contact your district agricultural extension officer today",
            "Reduce further investment in this season's crop until conditions improve",
            "Prioritise protecting already-planted areas over expanding new planting",
            "Document all losses for potential government or NGO relief support",
        ]
    },
    "Medium": {
        "Rainfall deficit": [
            "Monitor rainfall closely — check for updates every 3 days",
            "Prepare irrigation equipment in case drought conditions worsen",
            "Do not expand planting area until rainfall improves",
            "Consider drought-resistant varieties for any late planting",
            "Keep soil covered with mulch to retain moisture",
        ],
        "High pest pressure": [
            "Inspect all fields weekly — pest levels are rising",
            "Prepare pesticide stocks now before shortages occur",
            "Apply preventive treatment on highest-risk areas",
            "Report pest observations to extension officer for district monitoring",
        ],
        "Poor vegetation health (low NDVI)": [
            "Check soil moisture and nutrient levels",
            "Apply top-dressing fertiliser if growth appears stunted",
            "Increase irrigation if available — vegetation health is declining",
            "Monitor for early disease symptoms",
        ],
        "default": [
            "Conditions are borderline — monitor closely over the next two weeks",
            "Prepare contingency inputs (pesticide, irrigation equipment)",
            "Do not expand planted area this month",
            "Check in with your extension officer at the next scheduled visit",
            "Re-check your risk score in 14 days",
        ]
    },
    "Low": {
        "default": [
            "Conditions are currently favourable — continue normal farming schedule",
            "This is a good window for additional planting if land is available",
            f"Monitor pest levels as a precaution — early detection is always cheaper than late treatment",
            "Plan your harvest and marketing strategy — conditions support good yields",
            "Re-check your risk score in 30 days",
        ]
    }
}

CROP_NOTES = {
    "Maize":       "Maize is most vulnerable during tasselling and silking — prioritise water at those stages.",
    "Groundnuts":  "Groundnuts need consistent moisture during pod filling — drought at this stage causes severe losses.",
    "Sorghum":     "Sorghum is more drought-tolerant than maize, but high pest pressure at heading is critical.",
    "Sugar beans": "Sugar beans are sensitive to waterlogging and drought equally — balance is key.",
    "Sunflower":   "Sunflower needs water most during head formation — monitor soil moisture at that stage.",
    "Tomatoes":    "Tomatoes require consistent irrigation — irregular watering causes blossom drop and splitting.",
}


def get_recommendations(risk_level: str, dominant_factor: str, crop: str) -> list:
    """Return ranked list of recommendations for given risk level, dominant factor, and crop."""
    level_recs = RECS.get(risk_level, RECS["Low"])

    # Try factor-specific recs first, fall back to default
    recs = level_recs.get(dominant_factor, level_recs.get("default", []))

    # Add crop-specific note if available
    crop_note = CROP_NOTES.get(crop)
    if crop_note:
        recs = recs[:5] + [f"[{crop} note] {crop_note}"]

    return recs[:6]  # Max 6 recommendations
