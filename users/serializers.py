from rest_framework import serializers

from .models import Marketer, Influencer


class MarketerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Marketer
        fields = [
            "id",
            "username",
            "password",
            "phone",
            "mail",
            "company_name",
            "national_id",
            "company_code",
            "ceo_name",
            "telephone",
            "address"
        ]

    def create(self, validated_data):
        return Marketer.objects.create_marketer(**validated_data)


class InfluencerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Influencer
        fields = [
            "id",
            "username",
            "password",
            "phone",
            "mail",
            "instagram_id",
            "location",
            "is_general_page",
            "card_number",
            "account_number"
        ]

    def create(self, validated_data):
        return Influencer.objects.create_influencer(**validated_data)
