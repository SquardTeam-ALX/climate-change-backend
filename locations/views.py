# locations/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import State
from weather.services import fetch_weather  # adjust import if your service is in another app
from weather.serializers import WeatherSerializer  # adjust path as needed


@api_view(['GET'])
def get_nigerian_state_weather(request, state_name):
    # Normalize input (case-insensitive, handle FCT)
    try:
        if state_name.lower() == "fct":
            state = State.objects.get(abbreviation="FCT")
        else:
            # Try exact name first
            state = State.objects.get(name__iexact=state_name)
    except State.DoesNotExist:
        return Response(
            {"error": f"State '{state_name}' not found in Nigeria."},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        weather_data = fetch_weather(float(state.latitude), float(state.longitude))
        serializer = WeatherSerializer(weather_data)

        return Response({
            "location": {
                "state": state.name,
                "capital": state.capital,
                "abbreviation": state.abbreviation,
                "latitude": state.latitude,
                "longitude": state.longitude,
            },
            "weather": serializer.data
        })
    except Exception as e:
        return Response(
            {"error": "Failed to fetch weather data", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )