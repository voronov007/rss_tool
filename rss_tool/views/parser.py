from django.shortcuts import render
from django.views import View

from rss_tool.forms import RSSForm
from rss_tool.utils.parser import rss_xml_parser
from rss_tool.utils.validators import validate_url

# from .models import RSS
__all__ = [
    'UrlParserView'
]


class UrlParserView(View):
    template_name = 'rss_tool/parser.html'
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
        if "errors" in self.data:
            del self.data["errors"]

        # process form
        form = self.form_class(request.POST)
        if form.is_valid():
            url = validate_url(form.cleaned_data["rss_url"])
            if not url:
                errors.append("Incorrect RSS url address. Please fix it")

            if not errors:
                self.data["success"] = "RSS parsing started. Please, be patient"
                # show an empty form
                self.data["form"] = self.form_class()
                # run parsing
                rss_xml_parser(url, request.user.id)
                return render(request, self.template_name, self.data)
            else:
                self.data["errors"] = errors

        # show form with previously entered data
        self.data["form"] = form

        return render(request, self.template_name, self.data)
