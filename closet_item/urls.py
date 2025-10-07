from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet


app_name = 'closet_item'

router = DefaultRouter()
router.register('', ItemViewSet, basename='items')
