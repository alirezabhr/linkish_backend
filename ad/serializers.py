from rest_framework import serializers

from .models import Ad, InfAd


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

    def validated_image(self, image):
        print("image: ", image)


class InfAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfAd
        fields = '__all__'
