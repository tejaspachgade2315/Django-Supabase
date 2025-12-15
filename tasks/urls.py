"""
Task URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for the TaskViewSet
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    # CRUD endpoints via router
    path('', include(router.urls)),
    
    # Statistics endpoint for data visualization
    path('stats/', views.task_stats, name='task-stats'),
    
    # Third-party API integration endpoint
    path('weather/', views.weather_api, name='weather-api'),
]
