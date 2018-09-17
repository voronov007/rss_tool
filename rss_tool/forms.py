from django import forms


class RSSForm(forms.Form):
    rss_url = forms.URLField(label='RSS url', max_length=150)


class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', max_length=150)
    feed_id = forms.IntegerField(widget=forms.HiddenInput())

