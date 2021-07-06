from django.contrib import admin

from .models import User, Marketer, Influencer, OTP

# Register your models here.
admin.site.register(User)
admin.site.register(Marketer)
admin.site.register(Influencer)
admin.site.register(OTP)
