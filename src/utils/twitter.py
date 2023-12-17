import re

TWITTER_REPLACER = re.compile(r"https?://(twitter|x).com/(?P<user>[^/]+)/status/(?P<rest>\d+)")
TWITTER_REPLACER_RAW_STR = r"https://vxtwitter.com/\g<user>/status/\g<rest>"


def extract_tweet_url_list(text: str) -> list[str]:
    found = TWITTER_REPLACER.finditer(text)
    return [m.group(0) for m in found]


def replace_twitter_url_with_vx(text: str) -> str:
    return TWITTER_REPLACER.sub(TWITTER_REPLACER_RAW_STR, text)
