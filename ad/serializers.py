from rest_framework import serializers

from .models import Ad, InfAd, SuggestAd


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class SuggestAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestAd
        fields = '__all__'
        depth = 1


class InfAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfAd
        fields = '__all__'
