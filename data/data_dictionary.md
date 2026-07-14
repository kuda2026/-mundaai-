# Data Dictionary — MundaAI Training Dataset

**File**: `02_agriculture_climate_market_signals.csv`  
**Records**: 360 | **Provinces**: 10 | **Crops**: 6 | **Period**: January–June 2026

---

## Columns

| Column | Type | Description | Range / Values |
|--------|------|-------------|----------------|
| `month` | string | Calendar month of record | Jan, Feb, Mar, Apr, May, Jun |
| `province` | string | Zimbabwe province | 10 provinces |
| `district` | string | District within province | Multiple per province |
| `crop` | string | Crop type | Maize, Groundnuts, Sorghum, Sugar beans, Sunflower, Tomatoes |
| `rainfall_mm` | float | Rainfall received this month (millimetres) | 0 – ~200mm |
| `ndvi_proxy_0_1` | float | Normalised Difference Vegetation Index — proxy for crop/vegetation health | 0.0 (bare/dead) – 1.0 (lush) |
| `pest_incidents_reported` | int | Number of pest incidents reported in the district this month | 0 – 24 |
| `irrigation_coverage_pct` | float | Percentage of farmland with irrigation access | 0 – 100% |
| `input_availability_score_0_100` | float | Composite score of seed, fertiliser, pesticide availability | 0 (none) – 100 (fully available) |
| `avg_farmgate_price_usd_per_tonne` | float | Average price farmers receive at farmgate (USD per tonne) | Varies by crop |
| `estimated_yield_t_per_ha` | float | Estimated crop yield (tonnes per hectare) | 0 – ~5 t/ha |
| `climate_crop_risk_score_0_100` | float | Composite climate-crop risk score (higher = more dangerous) | 0 – 100 |
| `risk_level` | string | **TARGET VARIABLE** — categorical risk classification | Low, Medium, High |

---

## Target Variable Distribution

| Risk Level | Count | Percentage | Meaning |
|------------|-------|-----------|---------|
| Low | 172 | 47.8% | Conditions stable, normal farming activity safe |
| Medium | 173 | 48.1% | Conditions borderline, monitoring recommended |
| High | 15 | 4.2% | Conditions dangerous, immediate intervention needed |

> ⚠️ **Class imbalance**: Only 4.2% of records are High-risk. This is why CTGAN augmentation is used — to generate synthetic High-risk samples so the classifier learns to detect dangerous situations rather than ignoring them.

---

## High-Risk Hotspots (from analysis)

Districts with confirmed High-risk records in the dataset:

| District | Province | Crop | Risk Score | Month |
|---------|---------|------|-----------|-------|
| Masvingo | Masvingo | Groundnuts | 81.6 | May |
| Lupane | Matabeleland North | Groundnuts | 80.2 | May |
| Hwange | Matabeleland North | Groundnuts | 80.2 | Apr |
| Beitbridge | Matabeleland South | Tomatoes | 75.3 | May |
| Lupane | Matabeleland North | Sugar beans | 70.4 | May |
| Murehwa | Mashonaland East | Tomatoes | 73.4 | Jun |

---

## Features Used in Training

```python
FEATURES = [
    'rainfall_mm',
    'ndvi_proxy_0_1',
    'pest_incidents_reported',
    'irrigation_coverage_pct',
    'input_availability_score_0_100',
    'avg_farmgate_price_usd_per_tonne',
    'crop_encoded',       # label-encoded from 'crop'
    'province_encoded'    # label-encoded from 'province'
]

TARGET = 'risk_level'  # Low / Medium / High
```
