from rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    temperature = serializers.DictField()  # {'air': float, 'soil': float}
    humidity = serializers.FloatField()
    rainfall = serializers.FloatField()
    wind_speed = serializers.FloatField()
    uv_index = serializers.FloatField()
    soil_moisture = serializers.FloatField(allow_null=True)

# Add these new serializers
class CropRecommendationSerializer(serializers.Serializer):
    crop = serializers.CharField()
    score = serializers.FloatField()
    reasons = serializers.ListField(child=serializers.CharField())

class WeatherWithCropsSerializer(serializers.Serializer):
    location = serializers.DictField()
    weather = WeatherSerializer()
    recommended_crops = CropRecommendationSerializer(many=True)
    alerts = serializers.ListField(child=serializers.CharField())