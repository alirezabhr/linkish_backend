from django.urls import path
from users import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('obtain-token/', obtain_jwt_token),
    path('send-email/', views.send_otp_email),
    path('check-otp/', views.check_otp),
    path('signup/marketer/', views.MarketerSignup.as_view()),
    path('signup/influencer/', views.InfluencerSignup.as_view()),
    path('topic/', views.TopicView.as_view()),
    path('influencer/<int:pk>/', views.UpdateInfluencer.as_view()),
    path('change-pass/<int:pk>/', views.ChangePassword.as_view()),
]
