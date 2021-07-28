from django.contrib import admin

from .models import User, Marketer, Influencer, OTP, Topic, Withdraw

# Register your models here.
admin.site.register(User)
admin.site.register(Marketer)
admin.site.register(Influencer)
admin.site.register(OTP)
admin.site.register(Topic)
admin.site.register(Withdraw)
