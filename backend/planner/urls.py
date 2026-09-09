from django.urls import path

from .views import (
    TaskListCreateView,
    TaskDetailView,
    PlannerListListCreateView,
    PlannerListDetailView,
)


urlpatterns = [
    path(
        'tasks/',
        TaskListCreateView.as_view(),
        name='task-list-create'
    ),

    path(
        'tasks/<int:pk>/',
        TaskDetailView.as_view(),
        name='task-detail'
    ),

    path(
        'lists/',
        PlannerListListCreateView.as_view(),
        name='planner-list-list-create'
    ),

    path(
        'lists/<int:pk>/',
        PlannerListDetailView.as_view(),
        name='planner-list-detail'
    ),
]