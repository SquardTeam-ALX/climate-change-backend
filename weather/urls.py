from django.urls import path
from . import views

urlpatterns = [
    path('weather/<str:continent>/<str:country>/', views.get_weather_by_country, name='weather_by_country'),
    path('weather/all/', views.get_all_countries_weather, name='all_weather'),
    path('weather/with-crops/<str:continent>/<str:country>/', views.get_weather_with_crop_recommendations, name='weather_with_crops'),
]