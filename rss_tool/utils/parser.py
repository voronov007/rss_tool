import re
from xml.etree import ElementTree as etree

import requests
from django.utils.timezone import datetime as dt

from rss_tool.models.feed import Channel, Feed


def parser_exist(parsers: dict, url: str) -> bool:
    url = re.sub(r"(https?://)?(www\.)", "", url)
    exist = parsers.get(url)
    return True if exist else False


def rss_xml_parser_algemeen(url: str, user_id):
    datetime_pattern = "%a, %d %b %Y %X %z"
    r = requests.get(url)
    # print(r.text)

    # entire feed
    root = etree.fromstring(r.text)

    # get channel info
    channel = None
    for child in root:
        _channel_title = child.findtext("title")
        _channel_link = child.findtext("link")
        _last_build = dt.strptime(child.findtext("lastBuildDate"), datetime_pattern)
        channel = Channel.objects.filter(
            link=_channel_link, user__id=user_id
        ).first()
        if channel:
            # do not create new feeds if url time build repeats
            if channel.last_build >= _last_build:
                return

        if not channel:
            channel = Channel.objects.create(
                title=_channel_title, link=_channel_link, user_id=user_id,
                last_build=_last_build
            )
        break

    items = root.findall('channel/item')

    feeds = []
    for entry in items:
        # get description, url, and thumbnail
        desc = entry.findtext('description')
        title = entry.findtext('title')
        pub_date_str = entry.findtext('pubDate')
        pub_date = dt.strptime(pub_date_str, datetime_pattern)
        feeds.append(
            Feed(
                channel=channel, title=title,
                description=desc, pub_date=pub_date
            )
        )
        # feeds.append([title, desc, pub_date])
    Feed.objects.bulk_create(feeds)
