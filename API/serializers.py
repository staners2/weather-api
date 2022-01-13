from rest_framework import serializers
from .models import UserProfile, Error, Language, Histories, Cities, Weather

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        depth = 1
        fields = "__all__"

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        depth = 1
        fields = "__all__"

class HistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Histories
        depth = 2
        fields = "__all__"

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        depth = 1
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        depth = 1
        fields = "__all__"