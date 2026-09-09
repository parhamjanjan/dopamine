import os

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings'
)

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from rooms.middleware import JWTAuthMiddleware
from rooms.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    'http': django_asgi_app,

    'websocket': AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})