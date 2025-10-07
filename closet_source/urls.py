from django.urls import path

from . import views


app_name = 'closet_source'

urlpatterns = [
    path('sources/', views.SourceView.as_view()),
    path('sources/<pk>/', views.SourcePKView.as_view()),
    path("bulk/sources/", views.BulkSourceView.as_view()),

]