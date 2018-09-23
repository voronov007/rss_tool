from rss_tool.forms import RSSForm, CommentForm


def test_rss_form_ok():
    url = "test.com"
    form = RSSForm({"rss_url": url})
    assert form.is_valid() is True


def test_rss_form_error():
    url = "test/1/"
    form = RSSForm({"rss_url": url})
    assert form.is_valid() is False


def test_comment_form_ok():
    comment = "My first commit!"
    feed_id = 1
    form = CommentForm({"comment": comment, "feed_id": feed_id})
    assert form.is_valid() is True


def test_comment_form_error():
    comment = "Test"
    feed_id = 1
    form = CommentForm({"comment": comment, "feed_id": feed_id})
    assert form.is_valid() is False
