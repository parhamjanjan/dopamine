from django.contrib import admin

from .models import PlannerList, Task


@admin.register(PlannerList)
class PlannerListAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'user',
        'color',
        'created_at',
    )

    list_display_links = (
        'id',
        'name',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'name',
        'user__username',
        'user__email',
    )

    ordering = (
        '-created_at',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'user',
        'completed',
        'important',
        'category',
        'due_date',
        'start_time',
        'end_time',
        'planner_list',
        'created_at',
    )

    list_display_links = (
        'id',
        'title',
    )

    list_filter = (
        'completed',
        'important',
        'category',
        'reminder',
        'time_category',
        'due_date',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'category',
        'user__username',
        'user__email',
        'planner_list__name',
    )

    ordering = (
        '-created_at',
    )

    autocomplete_fields = (
        'user',
        'planner_list',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )