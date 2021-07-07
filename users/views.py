from random import randint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.decorators import api_view, permission_classes

from .models import Marketer, Influencer, OTP, Topic

from .serializers import MarketerSerializer, InfluencerSerializer, OTPSerializer, TopicSerializer


class MarketerSignup(APIView):
    query_set = Marketer.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MarketerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = self.request.data.get("password")
        token_serializer = JSONWebTokenSerializer(data={"email": user.email, "password": password})
        token_serializer.is_valid(raise_exception=True)
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
        token_serializer = JSONWebTokenSerializer(data={"email": user.email, "password": password})
        token_serializer.is_valid(raise_exception=True)
        res = {
            "token": token_serializer.validated_data.get("token"),
        }
        return Response(res, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_otp_email(request):
    data = request.data
    num = randint(10000, 99999)
    data['otp_code'] = num
    # todo send email
    try:
        obj = OTP.objects.get(email=request.data.get("email"))
        ser = OTPSerializer(obj, data=data)
    except:
        ser = OTPSerializer(data=data)

    if ser.is_valid():
        ser.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def check_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp_code")
    try:
        obj = OTP.objects.get(email=email)
    except:
        res = {
            "error": "this email didn't request otp code"
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    if otp != obj.otp_code:
        res = {
            "error": "otp is not correct"
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


class TopicView(APIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        ser = self.serializer_class(self.queryset.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
