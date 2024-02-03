from django.urls import path, re_path
from hack.views import SocialContentListAPIView, SocialContentStatisticsAPIView, InstagramListAPIView

urlpatterns = [
    path('contents/', SocialContentListAPIView.as_view()),
    path('statistics/', SocialContentStatisticsAPIView.as_view()),
    re_path('^instagram-contents', InstagramListAPIView.as_view()),
]