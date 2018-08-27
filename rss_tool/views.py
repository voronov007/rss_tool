from django.http import JsonResponse
from django.shortcuts import render, redirect
#
from .forms import RSSForm
# from .models import RSS


def url_parser(request):
    data = {
        'section': {'title': "RSS Tool"},
        'h1': "RSS Parser",
        'form': RSSForm()
    }
    errors = []
    if request.method == "POST":
        form = RSSForm(request.POST)
        if form.is_valid():
            # errors = person_data_validation(form.data)
            if not errors:
                data["success"] = "RSS parsing started. Please, be patient"
        else:
            data["form"] = form

    if errors:
        data["errors"] = errors

    return render(request, 'rss_tool/index.html', data)
