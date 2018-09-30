from django.contrib import admin

from rss_tool.models import Channel
from rss_tool.models import Comment
from rss_tool.models import Feed


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
