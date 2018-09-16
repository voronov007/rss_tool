from django.urls import path, re_path

from rss_tool import views

urlpatterns = [
    path('', views.UrlParserView.as_view(), name='index'),
    re_path(r'explore/?$', views.ExploreView.as_view(), name='explore'),
    re_path(
        r'feeds/(?P<user_id>[0-9]+)/?$',
        views.FeedsView.as_view(),
        name='feeds'
    ),
]
