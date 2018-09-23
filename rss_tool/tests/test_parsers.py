import pytest

from django.contrib.auth.models import User

from rss_tool.tasks import rss_xml_parser
from rss_tool.models.feed import Channel, Feed


pytestmark = pytest.mark.django_db

temp = ""


def patched_xml_response(url):
    class XMLPatch:
        text = """<?xml version="1.0" encoding="utf-8"?>
            <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
                <channel>
                    <title>NU - Algemeen</title>
                    <link>https://www.nu.nl/algemeen</link>
                    <description>Het laatste nieuws het eerst op NU.nl</description>
                    <language>nl-nl</language>
                    <copyright>Copyright (c) 2018, NU</copyright>
                    <lastBuildDate>Sun, 23 Sep 2018 16:14:10 +0200</lastBuildDate>
                    <ttl>60</ttl>
                    <item>
                        <title>Al 200.000 euro binnen voor slachtoffers treinongeluk Oss
                        </title>
                        <link>
                            https://www.nu.nl/binnenland/5476406/al-200000-euro-binnen-slachtoffers-treinongeluk-oss.html
                        </link>
                        <description>Met de inzamelingsactie voor de slachtoffers en
                            nabestaanden van het ongeluk in Oss is zondag al meer dan
                            200.000 euro opgehaald. Nick Nietveld uit Almere zette de actie
                            vrijdag op.
                        </description>
                        <pubDate>Sun, 23 Sep 2018 16:14:10 +0200</pubDate>
                    </item>
                    <item>
                        <title>Ajax begint zonder De Ligt aan topper tegen PSV, Eiting
                            opnieuw in basis
                        </title>
                        <link>
                            https://www.nu.nl/voetbal/5476409/ajax-begint-zonder-ligt-topper-psv-eiting-opnieuw-in-basis.html
                        </link>
                        <description>Ajax moet het zondagmiddag in de Eredivisie-topper in
                            het Philips Stadion tegen PSV opnieuw zonder de geblesseerde
                            aanvoerder Matthijs de Ligt doen. De thuisploeg begint in de
                            vertrouwde basisopstelling.
                        </description>
                        <pubDate>Sun, 23 Sep 2018 16:06:22 +0200</pubDate>
                    </item>
                    <item>
                        <title>'Witte Huis wil onderzoek instellen naar mededingingsregels
                            techbedrijven'
                        </title>
                        <link>
                            https://www.nu.nl/algemeen/5476253/witte-huis-wil-onderzoek-instellen-mededingingsregels-techbedrijven.html
                        </link>
                        <description>Het Witte Huis zou een onderzoek willen instellen naar
                            techbedrijven zoals Google en Facebook, met de vraag of zij
                            mededingingsregels hebben overtreden.
                        </description>
                        <pubDate>Sun, 23 Sep 2018 12:28:49 +0200</pubDate>
                    </item>
                </channel>
            </rss>
        """

    return XMLPatch()


def test_xml_parser_ok(mocker):
    mocker.patch(
        'rss_tool.tasks.parsing.requests.get', side_effect=patched_xml_response
    )

    email = "test@test.com"
    password = "test1234"
    user = User.objects.create(email=email, password=password, username=email)
    url = "https://test.com"
    rss_xml_parser(url=url, user_id=user.pk)

    assert Channel.objects.filter(user_id=user.pk).count() == 1
    assert Feed.objects.filter(channel__user_id=user.pk).count() == 3
