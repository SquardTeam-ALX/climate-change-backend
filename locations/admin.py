# locations/admin.py
from django.contrib import admin
from .models import State

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'capital', 'abbreviation', 'latitude', 'longitude')
    search_fields = ('name', 'capital')