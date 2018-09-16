from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('authentication.urls')),
    path('', include(('rss_tool.urls', 'rss_tool'), namespace='rss')),
    # re_path('^api/?$', include(('api.urls', 'api'), namespace='api'))
]

if settings.DEBUG and os.getenv("ENVIRONMENT", "test").lower() == "test":
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
