from django.conf import settings
from django.db import models


class PlannerList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planner_lists'
    )

    name = models.CharField(
        max_length=100
    )

    color = models.CharField(
        max_length=20,
        default='#7c3aed'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planner_tasks'
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        default=''
    )

    completed = models.BooleanField(
        default=False
    )

    important = models.BooleanField(
        default=False
    )

    category = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    start_time = models.TimeField(
        null=True,
        blank=True
    )

    end_time = models.TimeField(
        null=True,
        blank=True
    )

    reminder = models.CharField(
        max_length=30,
        default='none'
    )

    time_category = models.CharField(
        max_length=30,
        blank=True,
        default=''
    )

    study_time = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    planner_list = models.ForeignKey(
        PlannerList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title