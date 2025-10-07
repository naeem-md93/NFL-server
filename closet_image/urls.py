from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ImageViewSet

app_name = 'closet_image'

router = DefaultRouter()
router.register('', ImageViewSet, basename='images')
