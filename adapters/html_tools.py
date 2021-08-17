DEFAULT_BLACKLIST_TAGS = (
    "script",
    "time",
)

DEFAULT_UNWRAP_LIST_TAGS = (
    "div",
    "p",
    "span",
    "address",
    "article",
    "header",
    "footer",
)


def remove_buzz_attrs(soup):
    """Remove all attributes except some special tags."""
    for tag in soup.find_all(True):
        if tag.name == "a":
            tag.attrs = {
                "href": tag.attrs.get("href"),
            }
        elif tag.name == "img":
            tag.attrs = {
                "src": tag.attrs.get("src"),
            }
        else:
            tag.attrs = {}

    return soup


def remove_buzz_tags(
    soup, blacklist=DEFAULT_BLACKLIST_TAGS, unwrap_list=DEFAULT_UNWRAP_LIST_TAGS
):
    """Remove most of tags, leaves only tags significant for text analysis."""
    for tag in soup.find_all(True):
        if tag.name in blacklist:
            tag.decompose()
        elif tag.name in unwrap_list:
            tag.unwrap()
    return soup


def remove_all_tags(soup):
    """Unwrap all tags."""
    for tag in soup.find_all(True):
        tag.unwrap()
    return soup
