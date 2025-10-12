from django.urls import path

from . import views


app_name = 'closet'


urlpatterns = [
    path('closet/images/', views.ClosetImageView.as_view()),
    path("closet/items/", views.ClosetItemView.as_view()),
]