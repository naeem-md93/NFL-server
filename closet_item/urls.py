
from django.urls import path

from . import views


app_name = 'closet_item'


urlpatterns = [
    path('items/', views.ItemView.as_view()),
]