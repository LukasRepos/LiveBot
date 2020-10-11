import html
import random
from typing import Dict, Any

from hackernews import HackerNews

api = HackerNews()


def most_recent(_: Dict[str, Any]) -> str:
    new_story = random.choice(api.new_stories(limit=15))
    if new_story.text:
        return f"Todays most recent news are '{new_story.title}'! This is the article!\n{html.unescape(new_story.text)}"
    else:
        return f"Todays most recent news are '{new_story.title}'! See more in {new_story.url}"


def get_hottest(_: Dict[str, Any]) -> str:
    hottest_story = random.choice(api.top_stories(limit=15))
    if hottest_story.text:
        return f"Todays's hottest news is '{hottest_story.title}'! This is the article!\n{html.unescape(hottest_story.text)}"
    else:
        return f"Todays's hottest news is '{hottest_story.title}' See more in {hottest_story.url}"
