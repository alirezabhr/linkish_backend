from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import Influencer
from .models import Ad, InfAd, SuggestAd
from .serializers import AdSerializer, InfAdSerializer, SuggestAdSerializer
from .utils import get_random_link, is_after_24h


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
        ser = self.serializer_class(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class SuggestAdView(APIView):
    query_set = SuggestAd.objects.all()
    serializer_class = SuggestAdSerializer
    permission_classes = [AllowAny]

    def post(self, request, pk):
        get_object_or_404(Influencer, pk=pk)
        data = request.data
        data['influencer'] = pk
        ser = self.serializer_class(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def influencer_approved_ads(*args, **kwargs):
    pk = kwargs['pk']
    try:
        Influencer.objects.get(pk=pk)
    except:
        result = {
            "error": "influencer with this pk does not exist"
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    ad_id_list = []
    for suggested_ad in SuggestAd.objects.filter(influencer_id=pk, is_approved=True):
        inf_ad = InfAd.objects.get(suggested_ad=suggested_ad.id)
        ser = AdSerializer(suggested_ad.ad)
        result_item = {
            "short_link": inf_ad.short_link,
            "ad": ser.data,
        }
        ad_id_list.append(result_item)

    return Response(ad_id_list, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def influencer_disapproved_ads(*args, **kwargs):
    pk = kwargs['pk']
    try:
        Influencer.objects.get(pk=pk)
    except:
        result = {
            "error": "influencer with this pk does not exist"
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    ad_id_list = []
    for item in SuggestAd.objects.filter(influencer_id=pk, is_approved=False):
        ad_id_list.append(Ad.objects.get(id=item.ad.id))

    ser = AdSerializer(ad_id_list, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)


class InfluencerAdView(APIView):
    serializer_class = InfAdSerializer
    permission_classes = [AllowAny]

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
        data['short_link'] = get_random_link(InfAd)
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

    def get(self, request, pk):
        query_set = SuggestAd.objects.filter(influencer_id=pk)
        ser = SuggestAdSerializer(query_set, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class AdClickDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        short_url = kwargs["short_url"]
        obj = get_object_or_404(InfAd, short_link__exact=short_url)
        if is_after_24h(obj.approved_at):
            res = {
                "error": "this ad is expired"
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        url = obj.suggested_ad.ad.base_link
        obj.clicks += 1
        obj.suggested_ad.ad.clicks += 1
        obj.save()
        obj.suggested_ad.ad.save()
        return HttpResponseRedirect(url)
