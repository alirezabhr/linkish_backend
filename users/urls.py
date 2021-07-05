from django.urls import path
from users import views

urlpatterns = [
    path('marketer/signup', views.MarketerSignup.as_view()),
]
