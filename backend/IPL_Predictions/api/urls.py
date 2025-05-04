from django.urls import path
from .views import UploadMatchesAPIView, CurrentPredictionsAPIView

urlpatterns = [
    path("upload-matches/", UploadMatchesAPIView.as_view(), name="upload-matches"),
    path("current-predictions/", CurrentPredictionsAPIView.as_view(), name="current-predictions"),
]
