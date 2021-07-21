from django.urls import path, re_path
from ad import views


urlpatterns = [
    path('marketer/<int:pk>/', views.MarketerAdListView.as_view()),
    path('marketer/suggest/<int:pk>/', views.SuggestAdView.as_view()),
    path('inf/<int:pk>/', views.InfluencerAdView.as_view()),
    path('inf/<int:pk>/approved/', views.influencer_approved_ads),
    path('inf/<int:pk>/dis-approved/', views.influencer_disapproved_ads),
    re_path(r'^ia/(?P<short_url>[\w-]+)/$', views.AdClickDetailView.as_view()),
]
