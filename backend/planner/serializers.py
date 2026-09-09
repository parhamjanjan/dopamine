from rest_framework import serializers

from .models import Task, PlannerList


class PlannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannerList
        fields = [
            'id',
            'name',
            'color',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'important',
            'category',
            'due_date',
            'start_time',
            'end_time',
            'reminder',
            'time_category',
            'study_time',
            'planner_list',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]