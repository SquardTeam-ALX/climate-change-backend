# 🌾 AgriWeather API
## Real-Time Crop Recommendation System

**Production-ready backend API delivering hyper-local weather data and science-based crop recommendations for farmers worldwide.**

---

## 📋 Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Base URL](#base-url)
- [Endpoints](#endpoints)
- [Supported Locations](#supported-locations)
- [Tech Stack](#tech-stack)
- [Setup](#setup)

---

## Overview

AgriWeather provides intelligent crop recommendations by analyzing real-time weather conditions from multiple global data sources. The system evaluates:

| Factor | Details |
|--------|---------|
| **Air Temperature** | Optimal growth range per crop |
| **Soil Temperature & Moisture** | Root health and water availability |
| **Rainfall & Humidity** | Flood vs. drought tolerance |
| **UV Index** | Heat stress monitoring |
| **Seasonal Windows** | Respects regional planting calendars |

**Output:** Top 5 recommended crops with confidence scores (0–100) and actionable risk alerts.

**Use Cases:**
- Mobile agricultural advisory apps
- Government extension services
- Agribusiness decision-support platforms
- Precision farming applications

---

## Quick Start

### Base URL
```
http://127.0.0.1:8000/api/
```
*(Update domain and port when deploying to production)*

### Authentication
Public API (no authentication required for v1.0). Authentication will be implemented in future versions for user-specific farm data.

---

## Security & Credentials
All sensitive configuration is stored in environment variables (`.env`). Never commit API keys or secrets to version control.

---

## 🔌 API Endpoints

### 1. Get Weather + Crop Recommendations
```
GET /weather/nigeria/{state}/
```

Returns current weather data and top 5 recommended crops with confidence scores and risk alerts.

**Path Parameters:**
- `state` — Nigerian state name (e.g., `abia`, `kano`, `lagos`)

**Response Example:**
```json
{
  "location": {
    "state": "Lagos",
    "coordinates": {
      "latitude": 6.5244,
      "longitude": 3.3792
    }
  },
  "weather": {
    "timestamp": "2025-12-12T14:30:00Z",
    "temperature_air_celsius": 31.2,
    "temperature_soil_celsius": 29.8,
    "humidity_percent": 78,
    "rainfall_mm": 0.1,
    "wind_speed_kmh": 4.5,
    "uv_index": 9.1,
    "soil_moisture_percent": 42
  },
  "recommended_crops": [
    {
      "rank": 1,
      "crop_name": "Rice",
      "suitability_score": 96.4,
      "factors": ["Temperature optimal", "Moisture adequate", "Rainfall favorable"]
    },
    {
      "rank": 2,
      "crop_name": "Maize",
      "suitability_score": 92.1,
      "factors": ["Good growing conditions", "Soil moisture suitable"]
    }
  ],
  "alerts": [
    "High UV index: Limit fieldwork between 11:00–15:00",
    "High humidity: Monitor for fungal diseases"
  ]
}
```

**HTTP Status Codes:**
| Code | Meaning |
|------|---------|
| `200` | Success |
| `400` | Invalid location or parameter |
| `503` | Weather data temporarily unavailable |

---

### 2. Get Weather Data Only
```
GET /weather/nigeria/{state}/raw/
```

Returns raw weather data without crop analysis (lighter payload for dashboards).

---

### 3. Get All Supported Locations
```
GET /locations/
```

Returns list of all available Nigerian states and their geographic coordinates.

---

## 📍 Supported Locations

The API provides weather and crop recommendations for the following regions:

| Region | Coverage |
|--------|----------|
| **Africa** | All 36 Nigerian states + Federal Capital Territory (FCT Abuja) |
| **Asia** | India (national coverage) |
| **Europe** | Germany (national coverage) |
| **North America** | United States (national coverage) |
| **South America** | Brazil (national coverage) |
| **Oceania** | Australia (national coverage) |

### Nigeria Locations
All 36 states and the Federal Capital Territory are supported:

Abia, Adamawa, Akwa Ibom, Anambra, Bauchi, Bayelsa, Benue, Borno, Cross River, Delta, Ebonyi, Edo, Ekiti, Enugu, FCT Abuja, Gombe, Imo, Jigawa, Kaduna, Kano, Katsina, Kebbi, Kogi, Kwara, Lagos, Nasarawa, Niger, Ogun, Ondo, Osun, Oyo, Plateau, Rivers, Sokoto, Taraba, Yobe, Zamfara

Use the `/locations/` endpoint to retrieve the complete list with geographic coordinates for all supported regions.

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 5.0+ |
| **REST API** | Django REST Framework |
| **Language** | Python 3.10+ |
| **Weather Data** | Global meteorological APIs |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Caching** | Redis-ready architecture |
| **Crop Logic** | Rule-based expert system |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10 or higher
- Virtual environment (venv, conda, or similar)
- Git

### Local Development

**1. Clone and navigate to project:**
```bash
git clone <repository-url>
cd climate-change-backend
```

**2. Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**
Create a `.env` file in the project root with required API credentials.

**5. Run the development server:**
```bash
python manage.py migrate
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/api/`

---

## 📊 How It Works

### Recommendation Engine

The system uses a multi-factor scoring algorithm:

1. **Data Collection** — Fetch real-time weather data for the specified location
2. **Analysis** — Evaluate conditions against optimal ranges for each crop
3. **Scoring** — Calculate suitability score (0–100) based on all factors
4. **Ranking** — Return top 5 crops by score
5. **Alerts** — Generate risk warnings for extreme conditions

### Scoring Factors

The engine considers:
- **Air & Soil Temperature** — Optimal growth ranges per crop
- **Soil Moisture** — Water availability for root development
- **Rainfall** — Flood tolerance vs. drought tolerance
- **UV Index** — Heat and UV stress indicators
- **Humidity** — Disease and pest pressure
- **Seasonal Windows** — Respects regional planting calendars

---

## 🔒 Best Practices

✅ **Do:**
- Store API keys in environment variables
- Use HTTPS in production
- Implement rate limiting for public endpoints
- Cache responses to reduce API calls
- Log all weather queries for analytics

❌ **Don't:**
- Commit `.env` files to version control
- Expose API keys in frontend code
- Make unlimited requests without caching
- Trust single data sources
- Deploy with `DEBUG=True`

---

## 📈 Future Enhancements

- **User Accounts** — Save farm locations and preferences
- **7-Day Forecasts** — Predictive crop recommendations
- **Push Notifications** — Alert farmers to critical conditions
- **Mobile Applications** — Native iOS/Android apps
- **Machine Learning** — Advanced predictive models
- **Expanded Coverage** — Support for more countries
- **Admin Dashboard** — Manage locations and crop data
- **API Integrations** — Connect with farm management platforms

---

## 📞 Support & Feedback

For issues, feature requests, or questions about the API, please contact the development team or open an issue in the repository.

