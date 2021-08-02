import random

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import Influencer
from .models import Ad, InfAd, SuggestAd, AdViewerDetail
from .serializers import AdSerializer, InfAdSerializer, SuggestAdSerializer, SuggestAdSerializer2, InfAdSerializer2
from . import utils as adUtils
from users.utils import send_suggest_ad_email


# Create your views here.
class MarketerAdListView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdSerializer

    def get(self, request, pk):
        qs = Ad.objects.filter(marketer=pk)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        data = request.POST.copy()
        try:
            if not request.data["is_general"] and len(request.data["topics"]) == 0:
                res = {
                    "error": "topics list is empty!"
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            res = {
                "error": "key error"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        data['video'] = request.data['video']

        if not data['is_video']:
            data['video'] = ''
        else:
            if data['video'] == '':
                res = {
                    "error": "video field is empty"
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        data['image'] = request.data["image"]
        data['marketer'] = pk
        data['clicks'] = 0
        data['views'] = 0
        ser = self.serializer_class(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class SuggestAdView(APIView):
    query_set = SuggestAd.objects.all()
    serializer_class = SuggestAdSerializer2

    def post(self, request, pk):
        influencer = get_object_or_404(Influencer, pk=pk)
        data = request.data
        data['influencer'] = pk
        try:
            ad = get_object_or_404(Ad, pk=request.data['ad'])
        except Ad.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(data=data)
        if ser.is_valid():
            ser.save()
            send_suggest_ad_email(influencer.email, ad.title)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class InfluencerAdView(APIView):
    serializer_class = InfAdSerializer
    deduction_list = [10, 10, 10, 10, 10, 9, 9, 9, 9,
                      8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6,
                      5, 5, 4, 4, 3, 3, 2, 2, 1, 0]

    def post(self, request, pk):
        get_object_or_404(Influencer, pk=pk)
        data = request.data
        try:
            suggested_ad_id = data['suggested_ad']
        except:
            res = {
                "error": "suggested_ad needed"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        suggested_ad = get_object_or_404(SuggestAd, pk=suggested_ad_id)
        data['clicks'] = 0
        data['views'] = 0
        data['deduction'] = self.deduction_list[random.randint(0, len(self.deduction_list))]
        data['short_link'] = adUtils.get_random_link(InfAd)
        if suggested_ad.influencer.id != pk:
            res = {
                "error": "this ad didn't suggested to this influencer"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if suggested_ad.is_approved:
            res = {
                "error": "this ad was approved"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        inf_ad = self.serializer_class(data=data)
        if inf_ad.is_valid():
            suggested_ad.is_approved = True
            suggested_ad.save()
            inf_ad.save()
            return Response(inf_ad.data, status=status.HTTP_201_CREATED)
        return Response(inf_ad.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        get_object_or_404(Influencer, pk=pk)
        suggested_ad = get_object_or_404(SuggestAd, pk=request.data['suggested_ad'])
        serializer = SuggestAdSerializer(suggested_ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        query_set = SuggestAd.objects.filter(influencer_id=pk, is_rejected=False, is_reported=False)
        ser = SuggestAdSerializer(query_set, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ApprovedAdList(APIView):
    serializer_class = InfAdSerializer2
    query_set = InfAd.objects.all()

    def get(self, request, pk):
        qs = self.query_set.filter(suggested_ad__influencer=pk)
        ser = self.serializer_class(qs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class AdClickDetailView(APIView):
    permission_classes = [AllowAny]

    def create_ad_viewer_detail(self, inf_ad, ip, meta_data):
        ad_viewer_detail = AdViewerDetail()
        ad_viewer_detail.influencer_ad = inf_ad.id
        ad_viewer_detail.ip = ip
        ad_viewer_detail.http_referer = adUtils.get_http_referer(meta_data)
        ad_viewer_detail.save()

    def is_valid_request(self, inf_ad, ip, meta_data):
        http_referer = adUtils.get_http_referer(meta_data)
        if not http_referer or http_referer == "":
            return False
        if http_referer[-13:] != 'instagram.com':
            return False
        qs = AdViewerDetail.objects.filter(influencer_ad=inf_ad.id, ip=ip)
        if len(qs) != 0:
            return False
        return True

    def increaseViews(self, influencer_ad):
        influencer_ad.views += 1
        influencer_ad.suggested_ad.ad.views += 1
        influencer_ad.save()
        influencer_ad.suggested_ad.ad.save()

    def increaseClicks(self, influencer_ad):
        influencer_ad.clicks += 1
        influencer_ad.suggested_ad.ad.clicks += 1
        influencer_ad.save()
        influencer_ad.suggested_ad.ad.save()

    def get(self, request, *args, **kwargs):
        short_url = kwargs["short_url"]
        influencer_ad = get_object_or_404(InfAd, short_link__exact=short_url)

        if adUtils.is_after_24h(influencer_ad.approved_at):
            return render(request, 'expire_ad.html')
        else:
            ip = adUtils.get_client_ip(request)

            if adUtils.is_in_iran(ip):
                url = influencer_ad.suggested_ad.ad.base_link
                if self.is_valid_request(influencer_ad, ip, request.META):
                    self.increaseViews(influencer_ad=influencer_ad)
                    self.increaseClicks(influencer_ad=influencer_ad)
                else:
                    self.increaseViews(influencer_ad=influencer_ad)
                self.create_ad_viewer_detail(influencer_ad, ip, request.META)
                return HttpResponseRedirect(url)
            else:
                return render(request, 'vpn.html')


class InfluencerWallet(APIView):
    serializer_class = InfAdSerializer2
    query_set = InfAd.objects.all()

    def get(self, request, pk):
        qs = self.query_set.filter(suggested_ad__influencer=pk)
        result = []

        for item in qs:
            ser = self.serializer_class(item)
            res = {
                "income": int(item.clicks * ((100-item.deduction)/100)) * settings.COST_PER_CLICK,
                "influencer_ad": ser.data
            }
            result.append(res)

        return Response(result, status=status.HTTP_200_OK)
