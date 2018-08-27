from django import forms


class RSSForm(forms.Form):
    rss_url = forms.CharField(label='RSS url', max_length=150)
