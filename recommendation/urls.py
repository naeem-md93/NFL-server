from django.urls import path

from .views import RecommendationView


app_name = "recommendation"


urlpatterns = [
    path("recommendations/", view=RecommendationView.as_view())
]
