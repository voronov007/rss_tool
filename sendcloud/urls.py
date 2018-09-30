import os

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("", include("authentication.urls")),
    path("", include(("rss_tool.urls", "rss_tool"), namespace="rss")),
]

if settings.DEBUG and os.getenv("ENVIRONMENT", "test").lower() == "test":
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
