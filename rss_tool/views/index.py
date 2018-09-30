from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View

from rss_tool.models import Comment, Feed

__all__ = ["IndexView"]


class IndexView(View):
    template_name = "rss_tool/index.html"
    data = {"section": {"title": "RSS Tool"}, "h1": "My feeds"}

    def get(self, request, *args, **kwargs):
        feeds = (
            Feed.objects.select_related("channel")
            .prefetch_related("comments__author")
            .filter(channel__user_id=request.user.pk)
            .order_by("id")
        )

        # use pagination
        paginator = Paginator(feeds, 10)
        page = request.GET.get("page")
        feeds_per_page = paginator.get_page(page)

        has_next = feeds_per_page.has_next()
        has_previous = feeds_per_page.has_previous()

        output = {
            "feeds": feeds_per_page,
            "pagination": {
                "has_previous": has_previous,
                "has_next": has_next,
                "num_pages": feeds_per_page.paginator.num_pages,
                "number": feeds_per_page.number,
            },
        }
        if has_previous:
            output["pagination"][
                "previous_page_number"
            ] = feeds_per_page.previous_page_number()

        if has_next:
            output["pagination"][
                "next_page_number"
            ] = feeds_per_page.next_page_number()

        self.data.update(output)

        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        data = request.POST
        current_user = request.user
        feed_id = int(data.get("feed_id", 0))

        comment = data.get("comment")
        if not comment:
            return JsonResponse({"feed_id": feed_id, "success": False})

        Comment.objects.create(
            feed_id=feed_id, author_id=current_user.pk, text=comment
        )
        return JsonResponse(
            {
                "feed_id": feed_id,
                "success": True,
                "comment": comment,
                "email": current_user.email,
            }
        )
