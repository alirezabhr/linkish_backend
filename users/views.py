from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from .models import Marketer, Influencer

from .serializers import MarketerSerializer, InfluencerSerializer


class MarketerSignup(APIView):
    query_set = Marketer.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MarketerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = self.request.data.get("password")
        token_serializer = JSONWebTokenSerializer(data={"username": user.username, "password": password})
        token_serializer.is_valid(raise_exception=True)     # todo token is not correct in marketer
        res = {
            "token": token_serializer.validated_data.get("token"),
        }
        return Response(res, status=status.HTTP_201_CREATED)


class InfluencerSignup(APIView):
    query_set = Influencer.objects.all()
    permission_classes = [AllowAny]
    serializer_class = InfluencerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = self.request.data.get("password")
        token_serializer = JSONWebTokenSerializer(data={"username": user.username, "password": password})
        token_serializer.is_valid(raise_exception=True)
        res = {
            "token": token_serializer.validated_data.get("token"),
        }
        return Response(res, status=status.HTTP_201_CREATED)
