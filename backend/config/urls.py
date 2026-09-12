from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/accounts/',
        include('accounts.urls')
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'api/planner/',
        include('planner.urls')
    ),

    path(
        'api/rooms/',
        include('rooms.urls')
    ),
    
]


if settings.DEBUG:

    # Static files
    urlpatterns += staticfiles_urlpatterns()

    # Uploaded media files
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )