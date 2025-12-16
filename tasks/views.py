"""
Task Views - API endpoints for CRUD operations and statistics.
"""
import requests
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .serializers import TaskSerializer, TaskStatsSerializer
from .supabase import SupabaseConfigError, SupabaseRequestError, SupabaseRestClient


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet for Task CRUD operations.
    
    Endpoints:
    - GET /api/tasks/ - List all tasks
    - POST /api/tasks/ - Create a new task
    - GET /api/tasks/{id}/ - Retrieve a specific task
    - PUT /api/tasks/{id}/ - Update a task
    - DELETE /api/tasks/{id}/ - Delete a task
    """
    serializer_class = TaskSerializer

    def _client(self) -> SupabaseRestClient:
        return SupabaseRestClient.from_django_settings()

    def _table(self) -> str:
        return getattr(settings, "SUPABASE_TASKS_TABLE", "tasks_task")

    def _supabase_error_response(self, error: Exception) -> Response:
        if isinstance(error, SupabaseConfigError):
            return Response(
                {
                    "error": "Supabase is not configured",
                    "details": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if isinstance(error, SupabaseRequestError):
            return Response(
                {
                    "error": "Supabase request failed",
                    "details": error.detail,
                },
                status=error.status_code,
            )

        return Response(
            {"error": "Unexpected error", "details": str(error)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def list(self, request):
        """List tasks (optionally filtered by status / priority)."""
        try:
            params = {
                "select": "*",
                "order": "created_at.desc",
            }

            status_filter = request.query_params.get("status")
            if status_filter:
                params["status"] = f"eq.{status_filter}"

            priority_filter = request.query_params.get("priority")
            if priority_filter:
                params["priority"] = f"eq.{priority_filter}"

            data, _headers = self._client().request("GET", self._table(), params=params)
            return Response(data or [])
        except Exception as e:
            return self._supabase_error_response(e)

    def create(self, request):
        """Create a new task."""
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = dict(serializer.validated_data)
        payload.pop("id", None)
        payload.pop("created_at", None)
        payload.pop("updated_at", None)

        try:
            data, _headers = self._client().request(
                "POST",
                self._table(),
                json=payload,
                prefer="return=representation",
            )
            created = (data or [None])[0] if isinstance(data, list) else data
            return Response(created, status=status.HTTP_201_CREATED)
        except Exception as e:
            return self._supabase_error_response(e)

    def retrieve(self, request, pk=None):
        """Retrieve a task by id."""
        try:
            data, _headers = self._client().request(
                "GET",
                self._table(),
                params={"select": "*", "id": f"eq.{pk}", "limit": 1},
            )
            if not data:
                raise NotFound("Task not found")
            return Response(data[0])
        except Exception as e:
            return self._supabase_error_response(e)

    def update(self, request, pk=None):
        """Full update (treated as partial for simplicity)."""
        return self.partial_update(request, pk=pk)

    def partial_update(self, request, pk=None):
        """Partial update of a task."""
        serializer = TaskSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        payload = dict(serializer.validated_data)
        payload.pop("id", None)
        payload.pop("created_at", None)
        payload.pop("updated_at", None)

        try:
            data, _headers = self._client().request(
                "PATCH",
                self._table(),
                params={"id": f"eq.{pk}"},
                json=payload,
                prefer="return=representation",
            )
            if not data:
                raise NotFound("Task not found")
            return Response(data[0])
        except Exception as e:
            return self._supabase_error_response(e)

    def destroy(self, request, pk=None):
        """Delete a task."""
        try:
            self._client().request(
                "DELETE",
                self._table(),
                params={"id": f"eq.{pk}"},
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return self._supabase_error_response(e)


@api_view(['GET'])
def task_stats(request):
    """
    Get task statistics for data visualization.
    
    Returns counts of tasks by status and priority.
    """
    try:
        client = SupabaseRestClient.from_django_settings()
        table = getattr(settings, "SUPABASE_TASKS_TABLE", "tasks_task")

        stats = {
            "total_tasks": client.count(table),
            "pending": client.count(table, filters={"status": "eq.pending"}),
            "in_progress": client.count(table, filters={"status": "eq.in_progress"}),
            "completed": client.count(table, filters={"status": "eq.completed"}),
            "high_priority": client.count(table, filters={"priority": "eq.high"}),
            "medium_priority": client.count(table, filters={"priority": "eq.medium"}),
            "low_priority": client.count(table, filters={"priority": "eq.low"}),
        }

        serializer = TaskStatsSerializer(stats)
        return Response(serializer.data)
    except SupabaseConfigError as e:
        return Response(
            {"error": "Supabase is not configured", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except SupabaseRequestError as e:
        return Response(
            {"error": "Supabase request failed", "details": e.detail},
            status=e.status_code,
        )


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
