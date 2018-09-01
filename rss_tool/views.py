from django.shortcuts import render
from django.views import View

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


class UrlParserView(View):
    template_name = 'rss_tool/index.html'
    form_class = RSSForm
    data = {
        'section': {'title': "RSS Tool"},
        'h1': "RSS Parser"
    }

    def get(self, request, *args, **kwargs):
        self.data["form"] = self.form_class()
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        errors = []
        form = self.form_class(request.POST)
        if form.is_valid():
            # errors = person_data_validation(form.data)
            if not errors:
                self.data["success"] = "RSS parsing started. Please, be patient"
                return render(request, self.template_name, self.data)
            else:
                self.data["errors"] = errors

        self.data["form"] = form

        return render(request, self.template_name, self.data)
