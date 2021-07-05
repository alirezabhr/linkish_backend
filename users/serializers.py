from rest_framework import serializers

from .models import Marketer


class MarketerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marketer
        fields = '__all__'

        # read_only_fields = ("id",)
        #
        # def create(self, validated_data):
        #     return CustomUser(**validated_data)
        #
        # def update(self, instance, validated_data):
        #     instance.username = validated_data.get('username', instance.username)
        #     instance.password = validated_data.get('password', instance.password)
        #     instance.first_name = validated_data.get('first_name', instance.first_name)
        #     return instance
