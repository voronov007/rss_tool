from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channels"
    )
    title = models.CharField(max_length=50)
    link = models.URLField(max_length=150)
    last_build = models.DateTimeField()

    class Meta:
        unique_together = ("user", "link")


class Feed(models.Model):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="feeds"
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField()
