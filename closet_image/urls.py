from django.urls import path

from . import views


app_name = 'closet_image'


urlpatterns = [
    path('images/', views.ImageView.as_view()),
]