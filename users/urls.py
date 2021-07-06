from django.urls import path
from users import views

urlpatterns = [
    path('send-email/', views.send_otp_email),
    path('check-otp/', views.check_otp),
    path('signup/marketer/', views.MarketerSignup.as_view()),
    path('signup/influencer/', views.InfluencerSignup.as_view()),
]
