from django.urls import path
from users import views

urlpatterns = [
    path('signup/marketer/', views.MarketerSignup.as_view()),
    path('signup/influencer/', views.InfluencerSignup.as_view()),
]
