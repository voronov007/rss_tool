from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import datetime as dt


class Channel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channels"
    )
    title = models.CharField(max_length=50)
    link = models.URLField(max_length=150)
    last_build = models.DateTimeField()

    class Meta:
        unique_together = ("user", "link")

    def __str__(self):
        _date = self.last_build.strftime("%Y/%m/%d %X")
        return f"""
        {type(self).__name__}({self.link} {_date})
        """

    def __repr__(self):
        return self.__str__()


class Feed(models.Model):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="feeds"
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField()

    class Meta:
        unique_together = ("channel", "title", "pub_date")

    def __str__(self):
        _date = self.pub_date.strftime("%Y/%m/%d %X")
        return f"""
        {type(self).__name__}({self.channel.pk}, {self.title}, {_date})
        """

    def __repr__(self):
        return self.__str__()


class Comment(models.Model):
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=100)
    pub_date = models.DateTimeField(editable=False)

    def __str__(self):
        _date = self.pub_date.strftime("%Y/%m/%d %X")
        return f"""
        {type(self).__name__}({self.author.email}, {self.feed.pk})
        """

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = dt.now()
        return super().save(*args, **kwargs)


class Bookmark(models.Model):
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name="bookmarks"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookmarks"
    )

    class Meta:
        unique_together = ("feed", "user")
