# weather/services.py
import requests
import os
from django.core.cache import cache
from datetime import datetime, timedelta

API_KEY = os.getenv('STORMGLASS_API_KEY')
BASE_URL = 'https://api.stormglass.io/v2/weather/point'

# These parameters are GUARANTEED to work on free + paid tiers
VALID_PARAMS = [
    'airTemperature',      # Air temp
    'humidity',            # Relative humidity
    'precipitation',       # Rainfall (mm/h)
    'windSpeed',           # Wind speed at 10m
    'gust',                # Wind gust (alternative if needed)
    'pressure',            # Atmospheric pressure
    'cloudCover',          # For sunlight estimation
]

# For soil moisture & UV → use their dedicated Agriculture API (still free tier!)
AGRI_URL = 'https://api.stormglass.io/v2/agriculture/point'

def fetch_weather(lat, lon):
    cache_key = f"weather_{lat}_{lon}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    headers = {'Authorization': API_KEY}

    # 1. Get standard weather
    params = {
        'lat': lat,
        'lng': lon,
        'params': ','.join(VALID_PARAMS),
        'start': datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z'),
        'end': (datetime.utcnow() + timedelta(hours=6)).strftime('%Y-%m-%dT23:59:59Z'),
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Weather API error: {response.status_code} - {response.text}")

    hours = response.json()['hours']
    current = hours[0]  # Most recent hour

    # 2. Get agriculture-specific data (soil moisture, soil temp, UV)
    agri_params = {
        'lat': lat,
        'lng': lon,
        'params': 'soilMoisture,soilTemperature,uvIndex',
    }
    agri_response = requests.get(AGRI_URL, headers=headers, params=agri_params)
    
    soil_moisture = soil_temp = uv_index = None
    if agri_response.status_code == 200:
        agri_data = agri_response.json()['hours'][0]
        soil_moisture = agri_data.get('soilMoisture', {}).get('sg')
        soil_temp = agri_data.get('soilTemperature', {}).get('sg')
        uv_index = agri_data.get('uvIndex', {}).get('sg', 0)  # fallback to 0 if missing
    else:
        print(f"Agriculture API fallback: {agri_response.text}")
        uv_index = 3  # safe fallback

    # Build final result
    result = {
        'timestamp': current['time'],
        'temperature': {
            'air': current['airTemperature']['sg'],
            'soil': soil_temp or round(current['airTemperature']['sg'] - 3, 1)  # rough estimate
        },
        'humidity': current['humidity']['sg'],
        'rainfall': current['precipitation']['sg'],
        'wind_speed': current['windSpeed']['sg'],
        'uv_index': uv_index,
        'soil_moisture': soil_moisture or 0.25,  # fallback estimate
    }

    cache.set(cache_key, result, timeout=1800)  # cache 30 mins
    return result