from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Ad
from .serializers import AdSerializer


# Create your views here.
class CreateAdView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    qs = Ad.objects.all()
    serializer = AdSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        ser = self.serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class MarketerAdListView(APIView):
    serializer_class = AdSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        qs = Ad.objects.filter(marketer=pk)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
