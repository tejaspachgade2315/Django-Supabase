"""
Task Views - API endpoints for CRUD operations and statistics.
"""
import requests
from django.conf import settings
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskStatsSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task CRUD operations.
    
    Endpoints:
    - GET /api/tasks/ - List all tasks
    - POST /api/tasks/ - Create a new task
    - GET /api/tasks/{id}/ - Retrieve a specific task
    - PUT /api/tasks/{id}/ - Update a task
    - DELETE /api/tasks/{id}/ - Delete a task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Optionally filter tasks by status or priority.
        """
        queryset = Task.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority_filter = self.request.query_params.get('priority', None)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        return queryset


@api_view(['GET'])
def task_stats(request):
    """
    Get task statistics for data visualization.
    
    Returns counts of tasks by status and priority.
    """
    stats = {
        'total_tasks': Task.objects.count(),
        'pending': Task.objects.filter(status='pending').count(),
        'in_progress': Task.objects.filter(status='in_progress').count(),
        'completed': Task.objects.filter(status='completed').count(),
        'high_priority': Task.objects.filter(priority='high').count(),
        'medium_priority': Task.objects.filter(priority='medium').count(),
        'low_priority': Task.objects.filter(priority='low').count(),
    }
    
    serializer = TaskStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
def weather_api(request):
    """
    Third-party API integration example.
    
    Fetches current weather data from OpenWeatherMap API.
    This demonstrates integrating with an external REST API.
    
    Query Parameters:
    - city: City name (default: London)
    """
    city = request.query_params.get('city', 'London')
    api_key = settings.OPENWEATHER_API_KEY
    
    # If no API key is configured, return demo data
    if not api_key or api_key == 'demo':
        return Response({
            'city': city,
            'temperature': 15,
            'description': 'Demo mode - configure OPENWEATHER_API_KEY for real data',
            'humidity': 65,
            'wind_speed': 5.5,
            'is_demo': True,
        })
    
    try:
        # Call OpenWeatherMap API
        url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return Response({
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'is_demo': False,
        })
    
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to fetch weather data: {str(e)}'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
