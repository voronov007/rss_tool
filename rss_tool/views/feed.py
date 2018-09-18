from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Subquery, Count, Exists, OuterRef
from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View

from rss_tool.forms import CommentForm
from rss_tool.models import Feed, Bookmark, Comment

__all__ = ['FeedsView']


class FeedsView(View):
    form_class = CommentForm
    template_name = 'rss_tool/feed.html'

    def post(self, request, user_id):
        data = request.POST
        current_user = request.user

        # check if bookmark
        is_bookmark = data.get("bookmark")
        feed_id = int(data.get("feed_id", 0))
        if is_bookmark:
            bookmark, _created = Bookmark.objects.get_or_create(
                feed_id=feed_id, user_id=current_user.pk
            )
            if not _created:
                bookmark.delete()
                return JsonResponse({"feed_id": feed_id, "removed": True})
            return JsonResponse({"feed_id": feed_id, "added": True})

        # else if comment
        comment = data.get("comment")
        if not comment:
            return JsonResponse({"feed_id": feed_id, "success": False})

        Comment.objects.create(
            feed_id=feed_id, author_id=current_user.pk, text=comment
        )
        return JsonResponse(
            {
                "feed_id": feed_id, "success": True, "comment": comment,
                "email": current_user.email
            }
        )

    def get(self, request, user_id):
        current_user_id = request.user.pk
        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise Http404("User not exist")

        # get feeds and check if feed is in favorites
        bookmark = Bookmark.objects.filter(user_id=current_user_id, feed_id=OuterRef('pk'))
        feeds = Feed.objects.prefetch_related(
            'comments__author'
        ).filter(
            channel__user_id=user.pk
        ).annotate(
            is_favorite=Exists(bookmark)
        ).order_by("-pub_date")

        # use pagination
        paginator = Paginator(feeds, 25)
        page = request.GET.get('page')
        feeds_per_page = paginator.get_page(page)

        has_next = feeds_per_page.has_next()
        has_previous = feeds_per_page.has_previous()
        if current_user_id == user_id:
            h1 = "Your feeds"
        else:
            h1 = f"{user.email} feeds"
        for f in feeds_per_page:
            print(f, f.is_favorite)
        template_data = {
            "h1": h1,
            "email": user.email,
            "feeds": feeds_per_page,
            "pagination": {
                "has_previous": has_previous,
                "has_next": has_next,
                "num_pages": feeds_per_page.paginator.num_pages,
                "number": feeds_per_page.number
            }
        }

        return render(request, self.template_name, template_data)
