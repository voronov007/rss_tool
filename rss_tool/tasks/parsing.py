from xml.etree import ElementTree as etree

import requests
from django.utils.timezone import datetime as dt

from rss_tool.models.feed import Channel, Feed
from sendcloud.celery import app

dt_patterns = {1: "%a, %d %b %Y %X %z", 2: "%a, %d %b %Y %X %Z"}


@app.task()
def rss_xml_parser(url: str, user_id: int):
    datetime_pattern = None
    r = requests.get(url)
    # print(r.text)

    # entire feed
    root = etree.fromstring(r.text)

    # get channel info
    channel = None
    for child in root:
        _channel_title = child.findtext("title")
        _channel_link = child.findtext("link")
        if datetime_pattern is None:
            datetime_pattern = get_dt_pattern(child.findtext("lastBuildDate"))
            if datetime_pattern is None:
                print(f"Error. Datetime pattern was not found. Url: {url}")
                return

        _last_build = dt.strptime(
            child.findtext("lastBuildDate"), datetime_pattern
        )
        channel = Channel.objects.filter(
            link=_channel_link, user__id=user_id
        ).first()
        if channel:
            # do not create new feeds if url time build repeats
            if channel.last_build.timestamp() >= _last_build.timestamp():
                return

        if not channel:
            channel = Channel.objects.create(
                title=_channel_title,
                link=_channel_link,
                user_id=user_id,
                last_build=_last_build,
            )
        break

    items = root.findall("channel/item")

    feeds = []
    for entry in items:
        # get description, url, and thumbnail
        desc = entry.findtext("description")
        title = entry.findtext("title")
        pub_date_str = entry.findtext("pubDate")
        pub_date = dt.strptime(pub_date_str, datetime_pattern)
        feeds.append(
            Feed(
                channel=channel,
                title=title,
                description=desc,
                pub_date=pub_date,
            )
        )
    Feed.objects.bulk_create(feeds)


def get_dt_pattern(dt_string):
    for key, pattern in dt_patterns.items():
        try:
            dt.strptime(dt_string, pattern)
        except Exception as e:
            pass
        else:
            return pattern
