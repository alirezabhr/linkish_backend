from django.urls import path, re_path
from ad import views


urlpatterns = [
    path('marketer/<int:pk>/', views.MarketerAdListView.as_view()),
    path('marketer/suggest/<int:pk>/', views.SuggestAdView.as_view()),
    path('inf/<int:pk>/', views.InfluencerAdView.as_view()),
    path('inf/<int:pk>/approved/', views.ApprovedAdList.as_view()),
    re_path(r'^ia/(?P<short_url>[\w-]+)/$', views.AdClickDetailView.as_view()),
]
