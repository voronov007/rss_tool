from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include(('rss_tool.urls', 'rss_tool'), namespace='rss')),
    # re_path('^api/?$', include(('api.urls', 'api'), namespace='api'))
]
