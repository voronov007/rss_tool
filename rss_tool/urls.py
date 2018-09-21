from django.urls import path, re_path

from rss_tool import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'parser/?$', views.UrlParserView.as_view(), name='parser'),
    re_path(r'explore/?$', views.ExploreView.as_view(), name='explore'),
    re_path(r'favorites/?$', views.FavoritesView.as_view(), name='favorites'),
    re_path(
        r'feeds/(?P<user_id>[0-9]+)/?$',
        views.FeedsView.as_view(),
        name='feeds'
    ),
]
