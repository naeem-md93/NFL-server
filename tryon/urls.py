from django.urls import path

from .views import TryOnView


app_name = "tryon"


urlpatterns = [
    path("tryon/", view=TryOnView.as_view())
]
