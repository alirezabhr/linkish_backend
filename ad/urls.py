from django.urls import path, re_path
from ad import views


urlpatterns = [
    path('create/', views.CreateAdView.as_view()),
    path('<int:pk>/all/', views.MarketerAdListView.as_view()),
    path('inf/<int:pk>/', views.InfluencerAdView.as_view()),
    re_path(r'^ia/(?P<short_url>[\w-]+)/$', views.AdClickDetailView.as_view()),
]
