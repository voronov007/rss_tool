from rss_tool.utils.validators import validate_url


def test_validate_url_ok():
    url = "abcd.com"
    assert validate_url(url) == f"https://{url}"


def test_validate_url_error():
    url = "abcd/1/d"
    assert validate_url(url) is None

    url = "http://abcd.com?q=1"
    assert validate_url(url) is None
