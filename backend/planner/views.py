from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task, PlannerList
from .serializers import TaskSerializer, PlannerListSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        )


class PlannerListListCreateView(generics.ListCreateAPIView):
    serializer_class = PlannerListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlannerList.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class PlannerListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlannerListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlannerList.objects.filter(
            user=self.request.user
        )