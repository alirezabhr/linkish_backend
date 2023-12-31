from random import randint

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.decorators import api_view, permission_classes

from .models import Marketer, Influencer, OTP, Topic
from .serializers import MarketerSerializer, InfluencerSerializer, OTPSerializer, TopicSerializer, WithdrawSerializer
from . import utils as user_utils


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
            "id": user.id,
            "token": token_serializer.validated_data.get("token"),
        }
        return Response(res, status=status.HTTP_201_CREATED)


class InfluencerSignup(APIView):
    query_set = Influencer.objects.all()
    permission_classes = [AllowAny]
    serializer_class = InfluencerSerializer

    def post(self, request):
        try:
            if not request.data["is_general_page"] and len(request.data["topics"]) == 0:
                res = {
                    "error": "topics list is empty!"
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            res = {
                "error": "key error"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = self.request.data.get("password")
        token_serializer = JSONWebTokenSerializer(data={"email": user.email, "password": password})
        token_serializer.is_valid(raise_exception=True)
        res = {
            "id": user.id,
            "token": token_serializer.validated_data.get("token"),
        }
        return Response(res, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_otp_email(request):
    data = request.data
    num = randint(10000, 99999)
    data['otp_code'] = num
    try:
        user_utils.send_otp_email(num, request.data.get("email"))
    except:
        result = {
            "error": "can not send email"
        }
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

    def post(self, request):  # todo need to change permission for post or remove it
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        ser = self.serializer_class(self.queryset.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_influencer(request):
    try:
        influencer = Influencer.objects.get(pk=request.data['pk'])
    except:
        result = {
            "error": "pk is incorrect"
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    data = {
        "card_number": request.data['card_number'],
        "account_number": request.data['account_number']
    }
    ser = InfluencerSerializer(influencer, data=data)
    if ser.is_valid():
        return Response(ser.data, status=status.HTTP_200_OK)

    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateInfluencer(APIView):
    serializer_class = InfluencerSerializer
    query_set = Influencer.objects.all()

    def put(self, request, pk):
        influencer = get_object_or_404(Influencer, pk=pk)
        data = {}

        try:
            data['card_number'] = request.data['card_number']
            data['account_number'] = request.data['account_number']
        except:
            res = {
                "error": "card number or account number does not exist"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        data['email'] = influencer.email
        data['password'] = influencer.password
        data['instagram_id'] = influencer.instagram_id
        data['province'] = influencer.province
        data['city'] = influencer.city
        data['is_general_page'] = influencer.is_general_page
        ser = self.serializer_class(influencer, data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        influencer = get_object_or_404(Influencer, pk=pk)
        ser = self.serializer_class(influencer)
        return Response(ser.data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    serializer_class = InfluencerSerializer
    query_set = Influencer.objects.all()

    def put(self, request, pk):
        influencer = get_object_or_404(Influencer, pk=pk)
        data = {}

        try:
            current_pass = request.data['current_pass']
            new_pass = request.data['new_pass']
        except:
            res = {
                "error": "new_pass or current_pass does not exist"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if not influencer.check_password(current_pass):
            res = {
                "error": "current password is not correct"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        influencer.set_password(new_pass)
        influencer.save()
        data['password'] = influencer.password
        data['email'] = influencer.email
        data['instagram_id'] = influencer.instagram_id
        data['province'] = influencer.province
        data['city'] = influencer.city
        data['is_general_page'] = influencer.is_general_page
        ser = self.serializer_class(influencer, data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawView(APIView):
    serializer_class = WithdrawSerializer

    def post(self, request, pk):
        influencer = get_object_or_404(Influencer, pk=pk)
        data = {
            "influencer": pk,
            "amount": request.data["amount"]
        }
        ser = self.serializer_class(data=data)
        if ser.is_valid():
            try:
                user_utils.send_withdraw_email(influencer.email, request.data['amount'])
                ser.save()
                return Response(ser.data, status=status.HTTP_200_OK)
            except:
                result = {"error": "Sry, Withdraw was unsuccessful. Please try later"}
                return Response(result, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
