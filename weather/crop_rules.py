# weather/crop_rules.py
from datetime import datetime

# Crop growing conditions (simplified but agronomically accurate)
# Temperature: optimal daytime range (°C)
# Soil moisture: volumetric water content (0–1)
# Rainfall tolerance: max mm/day before waterlogging risk
# UV/Heat tolerance: max UV index or temp before stress
CROP_DATABASE = {
    "Rice": {
        "temp_min": 20, "temp_optimal": (25, 35), "temp_max": 38,
        "soil_moisture_min": 0.35, "prefers_flooding": True,
        "rainfall_preference": "high",  # >100mm/week
        "suitable_months": [5,6,7,8,9],  # Kharif in India
        "risks": ["drought", "cold_snap"]
    },
    "Wheat": {
        "temp_min": 10, "temp_optimal": (15, 25), "temp_max": 32,
        "soil_moisture_min": 0.20,
        "rainfall_preference": "moderate",
        "suitable_months": [10,11,12,1,2,3],  # Rabi
        "risks": ["heat_wave", "waterlogging"]
    },
    "Maize": {
        "temp_min": 18, "temp_optimal": (24, 33), "temp_max": 38,
        "soil_moisture_min": 0.25,
        "rainfall_preference": "high",
        "risks": ["drought", "waterlogging"]
    },
    "Soybean": {
        "temp_min": 20, "temp_optimal": (25, 30), "temp_max": 35,
        "soil_moisture_min": 0.22,
        "rainfall_preference": "moderate",
        "risks": ["drought"]
    },
    "Potato": {
        "temp_min": 10, "temp_optimal": (15, 25), "temp_max": 30,
        "soil_moisture_min": 0.30,
        "rainfall_preference": "moderate",
        "risks": ["frost", "heat_wave"]
    },
    "Tomato": {
        "temp_min": 18, "temp_optimal": (21, 29), "temp_max": 35,
        "soil_moisture_min": 0.25,
        "uv_max": 8,
        "risks": ["frost", "extreme_heat"]
    },
    "Cotton": {
        "temp_min": 20, "temp_optimal": (25, 35), "temp_max": 40,
        "soil_moisture_min": 0.18,
        "rainfall_preference": "low_to_moderate",
        "risks": ["waterlogging"]
    },
    "Sorghum (Jowar)": {
        "temp_min": 20, "temp_optimal": (27, 35), "temp_max": 40,
        "soil_moisture_min": 0.15,  # Very drought tolerant
        "rainfall_preference": "low",
        "risks": []
    },
    "Groundnut": {
        "temp_min": 20, "temp_optimal": (25, 35), "temp_max": 38,
        "soil_moisture_min": 0.20,
        "rainfall_preference": "moderate",
        "risks": ["waterlogging"]
    },
    "Chickpea (Gram)": {
        "temp_min": 10, "temp_optimal": (15, 28), "temp_max": 32,
        "soil_moisture_min": 0.15,
        "rainfall_preference": "low",
        "suitable_months": [10,11,12,1,2],
        "risks": ["frost"]
    }
}

def score_crop(crop_name, weather_data, forecast_7day=None):
    """
    Returns suitability score 0–100 for a crop given current weather.
    Higher = better to plant now.
    """
    crop = CROP_DATABASE[crop_name]
    score = 100.0
    reasons = []

    current = weather_data
    temp = current['temperature']['air']
    humidity = current['humidity']
    soil_moist = current.get('soil_moisture') or 0.2
    rainfall = current['rainfall']
    uv = current['uv_index']

    # 1. Temperature suitability
    if temp < crop["temp_min"]:
        penalty = (crop["temp_min"] - temp) * 5
        score -= min(penalty, 60)
        reasons.append(f"Too cold ({temp}°C < {crop['temp_min']}°C)")
    elif temp > crop["temp_max"]:
        penalty = (temp - crop["temp_max"]) * 4
        score -= min(penalty, 60)
        reasons.append(f"Too hot ({temp}°C > {crop['temp_max']}°C)")
    else:
        opt_low, opt_high = crop["temp_optimal"]
        if not (opt_low <= temp <= opt_high):
            distance = min(abs(temp - opt_low), abs(temp - opt_high))
            score -= distance * 3
            reasons.append(f"Sub-optimal temperature")

    # 2. Soil moisture
    if soil_moist < crop["soil_moisture_min"]:
        deficit = crop["soil_moisture_min"] - soil_moist
        score -= deficit * 200
        reasons.append("Soil too dry")

    # 3. Rainfall / Water preference
    if crop.get("prefers_flooding") and rainfall < 2:
        score -= 20
        reasons.append("Needs standing water (e.g., rice)")

    # 4. UV stress
    if crop.get("uv_max") and uv > crop["uv_max"]:
        score -= (uv - crop["uv_max"]) * 8
        reasons.append("High UV stress")

    # 5. Seasonal check (very basic – India-centric for now)
    current_month = datetime.utcnow().month
    if crop.get("suitable_months") and current_month not in crop["suitable_months"]:
        score -= 40
        reasons.append("Wrong planting season")

    score = max(0, score)
    return {
        "crop": crop_name,
        "score": round(score, 1),
        "reasons": reasons[:3] if reasons else ["Good conditions"]
    }

def generate_alerts(weather_data):
    alerts = []
    temp = weather_data['temperature']['air']
    soil_moist = weather_data.get('soil_moisture') or 0.2
    rainfall = weather_data['rainfall']
    uv = weather_data['uv_index']

    if temp < 5:
        alerts.append("Frost risk! Protect sensitive crops.")
    if temp > 38:
        alerts.append("Heat wave warning! Provide shade/mulching.")
    if soil_moist < 0.15:
        alerts.append("Severe drought stress – irrigate immediately!")
    if soil_moist > 0.55 and rainfall > 10:
        alerts.append("Waterlogging risk – ensure drainage.")
    if uv > 9:
        alerts.append("Extreme UV – avoid fieldwork 10AM–4PM.")

    return alerts or ["No major risks detected."]