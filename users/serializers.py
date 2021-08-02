from rest_framework import serializers

from .models import Topic, Marketer, Influencer, OTP, Withdraw


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
            "email",
            "password",
            "company_name",
            "national_id",
            "company_code",
            "ceo_name",
            "telephone",
            "address",
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
            "email",
            "password",
            "instagram_id",
            "province",
            "city",
            "is_general_page",
            "card_number",
            "account_number",
            "topics",
        ]

    def create(self, validated_data):
        return Influencer.objects.create_influencer(**validated_data)


class OTPSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = OTP
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class WithdrawSerializer(serializers.ModelSerializer):
    request_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = Withdraw
        fields = '__all__'
