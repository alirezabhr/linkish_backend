from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Ad, InfAd
from .serializers import AdSerializer, InfAdSerializer
from .utils import get_random_link


# Create your views here.
class MarketerAdListView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        qs = Ad.objects.filter(marketer=pk)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        data = request.data
        data['marketer'] = pk
        data['clicks'] = 0
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class InfluencerAdView(APIView):
    serializer_class = InfAdSerializer
    queryset = InfAd.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, pk):
        data = request.data
        data['influencer'] = pk
        data['clicks'] = 0
        data['short_link'] = get_random_link(InfAd)

        inf_ad = self.serializer_class(data=data)
        if inf_ad.is_valid():
            inf_ad.save()
            return Response(inf_ad.data, status=status.HTTP_201_CREATED)
        return Response(inf_ad.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        ser = self.serializer_class(self.queryset.filter(influencer=pk), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class AdClickDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        short_url = kwargs["short_url"]
        obj = get_object_or_404(InfAd, short_link__exact=short_url)
        url = obj.ad.base_link
        return HttpResponseRedirect(url)
