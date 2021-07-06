from django.urls import path
from ad import views


urlpatterns = [
    path('create/', views.CreateAdView.as_view(), name='file-upload'),
]
