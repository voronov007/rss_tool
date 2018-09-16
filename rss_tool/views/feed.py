from django.contrib.auth.models import User
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from django.views import View

from rss_tool.models import Feed


__all__ = ['FeedsView']


class FeedsView(View):
    template_name = 'rss_tool/feed.html'

    def get(self, request, user_id):
        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise Http404("User not exist")
        feeds = Feed.objects.prefetch_related('comments').filter(
            channel__user_id=user.pk
        ).order_by("-pub_date")

        # use pagination
        paginator = Paginator(feeds, 25)
        page = request.GET.get('page')
        feeds_per_page = paginator.get_page(page)

        has_next = feeds_per_page.has_next()
        has_previous = feeds_per_page.has_previous()
        if request.user.pk == user_id:
            h1 = "Your feeds"
        else:
            h1 = f"{user.email} feeds"
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

        # for f in feeds_per_page:
        #     template_data["feeds"].append(
        #         {"title": f.title, "description": f.description, "id": f.pk}
        #     )

        return render(request, self.template_name, template_data)
