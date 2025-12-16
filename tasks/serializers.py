"""Task Serializers.

The Tasks API is backed by Supabase (PostgREST), so we validate and serialize
plain dictionaries rather than Django ORM model instances.
"""

from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False, default="")
    priority = serializers.ChoiceField(choices=["low", "medium", "high"], required=False, default="medium")
    status = serializers.ChoiceField(
        choices=["pending", "in_progress", "completed"], required=False, default="pending"
    )
    due_date = serializers.DateField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class TaskStatsSerializer(serializers.Serializer):
    """
    Serializer for task statistics (used in dashboard).
    """
    total_tasks = serializers.IntegerField()
    pending = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    completed = serializers.IntegerField()
    high_priority = serializers.IntegerField()
    medium_priority = serializers.IntegerField()
    low_priority = serializers.IntegerField()
