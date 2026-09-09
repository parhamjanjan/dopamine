from django.urls import path

from .views import (
    StudyRoomListCreateView,
    StudyRoomDetailView,
    JoinStudyRoomView,
    LeaveStudyRoomView,
    StartStudyView,
    StopStudyView,
    StudyHeartbeatView,
)


urlpatterns = [
    path(
        '',
        StudyRoomListCreateView.as_view(),
        name='room-list-create'
    ),

    path(
    '<int:room_id>/heartbeat/',
    StudyHeartbeatView.as_view(),
    name='study-heartbeat'
    ),

    path(
        '<int:room_id>/',
        StudyRoomDetailView.as_view(),
        name='room-detail'
    ),

    path(
        '<int:room_id>/join/',
        JoinStudyRoomView.as_view(),
        name='room-join'
    ),

    path(
        '<int:room_id>/leave/',
        LeaveStudyRoomView.as_view(),
        name='room-leave'
    ),

    path(
        '<int:room_id>/start-study/',
        StartStudyView.as_view(),
        name='start-study'
    ),

    path(
        '<int:room_id>/stop-study/',
        StopStudyView.as_view(),
        name='stop-study'
    ),
]