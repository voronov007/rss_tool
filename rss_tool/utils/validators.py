import re


def validate_url(url: str):
    """
    Description: if url is correct => return url, else return None
    url examples:
     OK: google.com
     ERROR: google.com?search=True
     ERROR: http://aaaaasdsa
    """
    is_matched = re.match(r"^(https?:\/\/)?(\w+\.\w+)+(\/\w+\/?)*$", url)
    if not is_matched:
        return

    if not url.startswith("http"):
        url = f"http://{url}"

    return url
