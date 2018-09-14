from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View


# from .models import RSS


class ExploreView(View):
    template_name = 'rss_tool/explore.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
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
            explore_data["users"].append({"email": u.email, "feeds": 1})
        return render(request, self.template_name, explore_data)
