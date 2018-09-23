from django import forms


class RSSForm(forms.Form):
    rss_url = forms.URLField(label='RSS url', min_length=5, max_length=150)


class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', min_length=10, max_length=150)
    feed_id = forms.IntegerField(widget=forms.HiddenInput())
