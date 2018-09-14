from django.urls import path, re_path

from rss_tool import views

urlpatterns = [
    path('', views.UrlParserView.as_view(), name='index'),
    re_path('explore/?$', views.ExploreView.as_view(), name='explore'),
]
