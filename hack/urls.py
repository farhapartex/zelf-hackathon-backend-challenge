from django.urls import path
from hack.views import SocialContentListAPIView, SocialContentStatisticsAPIView

urlpatterns = [
    path('contents/', SocialContentListAPIView.as_view()),
    path('statistics/', SocialContentStatisticsAPIView.as_view()),
    # path("api/v1/", include("hack.urls")),
]