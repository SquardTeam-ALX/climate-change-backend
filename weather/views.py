from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeatherSerializer, WeatherWithCropsSerializer
from .services import fetch_weather
from .crop_rules import CROP_DATABASE, score_crop, generate_alerts

SELECTED_COUNTRIES = {
    "North America": {"USA": {"lat": 39.8283, "lon": -98.5795}},
    "South America": {"Brazil": {"lat": -14.2350, "lon": -51.9253}},
    "Europe": {"Germany": {"lat": 51.1657, "lon": 10.4515}},
    "Asia": {"India": {"lat": 20.5937, "lon": 78.9629}},
    "Africa": {"Nigeria": {"lat": 9.0765, "lon": 8.6753}},
    "Oceania": {"Australia": {"lat": -25.2744, "lon": 133.7751}},
}

@api_view(['GET'])
def get_weather_by_country(request, continent, country):
    if continent not in SELECTED_COUNTRIES or country not in SELECTED_COUNTRIES[continent]:
        return Response({'error': 'Invalid continent/country'}, status=status.HTTP_404_NOT_FOUND)
    
    lat = SELECTED_COUNTRIES[continent][country]['lat']
    lon = SELECTED_COUNTRIES[continent][country]['lon']
    
    try:
        data = fetch_weather(lat, lon)
        serializer = WeatherSerializer(data)
        return Response({
            'location': {'continent': continent, 'country': country, 'lat': lat, 'lon': lon},
            'weather': serializer.data
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_countries_weather(request):
    results = {}
    for continent, countries in SELECTED_COUNTRIES.items():
        results[continent] = {}
        for country, coords in countries.items():
            data = fetch_weather(coords['lat'], coords['lon'])
            serializer = WeatherSerializer(data)
            results[continent][country] = serializer.data
    return Response(results)

@api_view(['GET'])
def get_weather_with_crop_recommendations(request, continent, country):
    if continent not in SELECTED_COUNTRIES or country not in SELECTED_COUNTRIES[continent]:
        return Response({'error': 'Invalid continent/country'}, status=404)

    coords = SELECTED_COUNTRIES[continent][country]
    lat, lon = coords['lat'], coords['lon']

    try:
        weather = fetch_weather(lat, lon)
        
        # Generate recommendations
        recommendations = []
        for crop_name in CROP_DATABASE.keys():
            scored = score_crop(crop_name, weather)
            recommendations.append(scored)
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        top_crops = recommendations[:5]  # Top 5

        alerts = generate_alerts(weather)

        response_data = {
            "location": {
                "continent": continent,
                "country": country,
                "lat": lat,
                "lon": lon
            },
            "weather": weather,
            "recommended_crops": top_crops,
            "alerts": alerts
        }

        serializer = WeatherWithCropsSerializer(response_data)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)