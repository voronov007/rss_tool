from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View

from rss_tool.forms import CommentForm
from rss_tool.models import Feed, Bookmark, Comment

__all__ = ['FavoritesView']


class FavoritesView(View):
    form_class = CommentForm
    template_name = 'rss_tool/favorites.html'

    def get(self, request):
        current_user_id = request.user.pk

        # get feeds and check if feed is in favorites
        feeds = Feed.objects.prefetch_related(
            'comments__author'
        ).select_related(
            "channel__user"
        ).filter(
            bookmarks__user_id=current_user_id
        ).order_by("-pub_date")

        # use pagination
        paginator = Paginator(feeds, 10)
        page = request.GET.get('page')
        feeds_per_page = paginator.get_page(page)

        has_next = feeds_per_page.has_next()
        has_previous = feeds_per_page.has_previous()

        template_data = {
            "h1": "Favorites",
            "feeds": feeds_per_page,
            "pagination": {
                "has_previous": has_previous,
                "has_next": has_next,
                "num_pages": feeds_per_page.paginator.num_pages,
                "number": feeds_per_page.number
            }
        }

        return render(request, self.template_name, template_data)

    def post(self, request):
        data = request.POST
        current_user = request.user

        # check if bookmark
        is_bookmark = data.get("bookmark")
        feed_id = int(data.get("feed_id", 0))
        if is_bookmark:
            bookmark = Bookmark.objects.filter(
                feed_id=feed_id, user_id=current_user.pk
            ).first()
            if bookmark:
                bookmark.delete()
                return JsonResponse({"feed_id": feed_id, "removed": True})
            return JsonResponse({"feed_id": feed_id, "removed": False})

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
