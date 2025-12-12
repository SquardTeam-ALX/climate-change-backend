from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeatherSerializer, WeatherWithCropsSerializer
from .services import fetch_weather
from .crop_rules import CROP_DATABASE, score_crop, generate_alerts

# Central country/state database — clean and easy to extend
SELECTED_COUNTRIES = {
    "North America": {
        "USA": {"lat": 39.8283, "lon": -98.5795},
    },
    "South America": {
        "Brazil": {"lat": -14.2350, "lon": -51.9253},
    },
    "Europe": {
        "Germany": {"lat": 51.1657, "lon": 10.4515},
    },
    "Asia": {
        "India": {"lat": 20.5937, "lon": 78.9629},
    },
    "Africa": {
        "Nigeria - Abia":           {"lat": 5.4527,  "lon": 7.5247},
        "Nigeria - Adamawa":        {"lat": 9.3265,  "lon": 12.3984},
        "Nigeria - Akwa Ibom":      {"lat": 4.9290,  "lon": 7.9278},
        "Nigeria - Anambra":        {"lat": 6.2209,  "lon": 7.0684},
        "Nigeria - Bauchi":         {"lat": 10.7761, "lon": 9.9992},
        "Nigeria - Bayelsa":        {"lat": 4.7719,  "lon": 6.0699},
        "Nigeria - Benue":          {"lat": 7.3369,  "lon": 8.7404},
        "Nigeria - Borno":          {"lat": 11.5097, "lon": 13.1239},
        "Nigeria - Cross River":    {"lat": 4.9600,  "lon": 8.3300},
        "Nigeria - Delta":          {"lat": 5.7046,  "lon": 5.9350},
        "Nigeria - Ebonyi":         {"lat": 6.2649,  "lon": 8.0137},
        "Nigeria - Edo":            {"lat": 6.6342,  "lon": 5.9304},
        "Nigeria - Ekiti":          {"lat": 7.7188,  "lon": 5.3103},
        "Nigeria - Enugu":          {"lat": 6.4584,  "lon": 7.5464},
        "Nigeria - FCT Abuja":      {"lat": 9.0765,  "lon": 7.3986},
        "Nigeria - Gombe":          {"lat": 10.2791, "lon": 11.1715},
        "Nigeria - Imo":            {"lat": 5.5720,  "lon": 7.0588},
        "Nigeria - Jigawa":         {"lat": 12.2280, "lon": 9.5616},
        "Nigeria - Kaduna":         {"lat": 10.5105, "lon": 7.4165},
        "Nigeria - Kano":           {"lat": 12.0022, "lon": 8.5920},
        "Nigeria - Katsina":        {"lat": 12.9194, "lon": 7.6000},
        "Nigeria - Kebbi":          {"lat": 12.4505, "lon": 4.1996},
        "Nigeria - Kogi":           {"lat": 7.7337,  "lon": 6.6906},
        "Nigeria - Kwara":          {"lat": 8.9669,  "lon": 4.3874},
        "Nigeria - Lagos":          {"lat": 6.5244,  "lon": 3.3792},
        "Nigeria - Nasarawa":       {"lat": 8.5333,  "lon": 7.7000},
        "Nigeria - Niger":          {"lat": 9.6000,  "lon": 6.5500},
        "Nigeria - Ogun":           {"lat": 7.0000,  "lon": 3.5833},
        "Nigeria - Ondo":           {"lat": 7.1000,  "lon": 4.8333},
        "Nigeria - Osun":           {"lat": 7.5624,  "lon": 4.5200},
        "Nigeria - Oyo":            {"lat": 8.1574,  "lon": 3.6147},
        "Nigeria - Plateau":        {"lat": 9.2182,  "lon": 9.5179},
        "Nigeria - Rivers":         {"lat": 4.8156,  "lon": 7.0498},
        "Nigeria - Sokoto":         {"lat": 13.0667, "lon": 5.2333},
        "Nigeria - Taraba":         {"lat": 8.0000,  "lon": 10.5000},
        "Nigeria - Yobe":           {"lat": 12.1871, "lon": 11.7068},
        "Nigeria - Zamfara":        {"lat": 12.1222, "lon": 6.2333},
    },
    "Oceania": {
        "Australia": {"lat": -25.2744, "lon": 133.7751},
    },
}

@api_view(['GET'])
def get_weather_by_country(request, continent, country):
    if continent not in SELECTED_COUNTRIES or country not in SELECTED_COUNTRIES[continent]:
        return Response(
            {"error": "Invalid continent or location. Check spelling and spaces."},
            status=status.HTTP_404_NOT_FOUND
        )

    coords = SELECTED_COUNTRIES[continent][country]
    lat, lon = coords['lat'], coords['lon']

    try:
        data = fetch_weather(lat, lon)
        serializer = WeatherSerializer(data)
        return Response({
            "location": {
                "continent": continent,
                "country": country.replace(" - ", " "),  # Make display nicer
                "lat": lat,
                "lon": lon
            },
            "weather": serializer.data
        })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_countries_weather(request):
    results = {}
    for continent, locations in SELECTED_COUNTRIES.items():
        results[continent] = {}
        for name, coords in locations.items():
            try:
                data = fetch_weather(coords['lat'], coords['lon'])
                serializer = WeatherSerializer(data)
                results[continent][name.replace(" - ", " ")] = serializer.data
            except Exception as e:
                results[continent][name.replace(" - ", " ")] = {"error": str(e)}
    return Response(results)


@api_view(['GET'])
def get_weather_with_crop_recommendations(request, continent, country):
    if continent not in SELECTED_COUNTRIES or country not in SELECTED_COUNTRIES[continent]:
        return Response(
            {"error": "Location not found. Use exact name like 'Nigeria - Kano' (with space-dash-space)."},
            status=status.HTTP_404_NOT_FOUND
        )

    coords = SELECTED_COUNTRIES[continent][country]
    lat, lon = coords['lat'], coords['lon']

    try:
        weather = fetch_weather(lat, lon)

        # Generate crop recommendations
        recommendations = [
            score_crop(crop_name, weather)
            for crop_name in CROP_DATABASE.keys()
        ]
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        top_crops = recommendations[:5]

        alerts = generate_alerts(weather)

        response_data = {
            "location": {
                "continent": continent,
                "country": country.replace(" - ", " "),  # Clean display name
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
        return Response({"error": f"Weather service error: {str(e)}"}, status=500)