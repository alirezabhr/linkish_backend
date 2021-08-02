from rest_framework import serializers

from .models import Ad, InfAd, SuggestAd, AdViewerDetail


class AdSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'


class SuggestAdSerializer2(serializers.ModelSerializer):
    suggested_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = SuggestAd
        fields = '__all__'


class SuggestAdSerializer(serializers.ModelSerializer):
    suggested_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = SuggestAd
        fields = '__all__'
        depth = 1


class InfAdSerializer(serializers.ModelSerializer):
    approved_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = InfAd
        fields = '__all__'


class InfAdSerializer2(serializers.ModelSerializer):
    approved_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = InfAd
        fields = '__all__'
        depth = 2


class AdViewerDetailSerializer(serializers.ModelSerializer):
    viewed_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = AdViewerDetail
        fields = '__all__'
