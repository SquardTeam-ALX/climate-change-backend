from django.urls import path, include
from . import views

urlpatterns = [
    path('nigeria/<str:state_name>/', views.get_nigerian_state_weather, name='nigerian_state_weather'),
]


