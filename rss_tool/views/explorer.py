from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from django.views import View


# from .models import RSS


class ExploreView(View):
    template_name = 'rss_tool/explore.html'

    def get(self, request, *args, **kwargs):
        # get users with at least 1 feed
        users = User.objects.annotate(
            feeds_count=Count('channels__feeds')
        ).filter(
            Q(feeds_count__gte=1), ~Q(id=request.user.pk)
        ).all()

        # use pagination
        paginator = Paginator(users, 25)
        page = request.GET.get('page')
        users_per_page = paginator.get_page(page)

        has_next = users_per_page.has_next()
        has_previous = users_per_page.has_previous()

        explore_data = {
            "h1": "Users and Feeds",
            "users": [],
            "pagination": {
                "has_previous": has_previous,
                "has_next": has_next,
                "num_pages": users_per_page.paginator.num_pages,
                "number": users_per_page.number
            }
        }
        if has_previous:
            explore_data["pagination"]["previous_page_number"] = users_per_page.previous_page_number()

        if has_next:
            explore_data["pagination"]["next_page_number"] = users_per_page.next_page_number()

        for u in users_per_page:
            explore_data["users"].append(
                {"email": u.email, "feeds": u.feeds_count, "id": u.pk}
            )

        return render(request, self.template_name, explore_data)
