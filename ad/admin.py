from django.contrib import admin

from .models import Ad, InfAd, SuggestAd, AdViewerDetail

# Register your models here.
admin.site.register(Ad)
admin.site.register(SuggestAd)
admin.site.register(InfAd)
admin.site.register(AdViewerDetail)
