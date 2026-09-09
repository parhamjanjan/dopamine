from django.urls import path

from .consumers import StudyRoomConsumer


websocket_urlpatterns = [
    path(
        'ws/rooms/<int:room_id>/',
        StudyRoomConsumer.as_asgi(),
    ),
]