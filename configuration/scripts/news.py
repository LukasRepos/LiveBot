import html
from collections import deque

from hackernews import HackerNews

api = HackerNews()


def most_recent(_: deque, __: str, ___: str) -> str:
    new_story = api.new_stories(limit=1)[0]
    if new_story.text:
        return f"Todays hottest news is '{new_story.title}'! This is the article!\n{new_story.text}"
    else:
        return f"Todays hottest news is '{new_story.title}'! See more in {new_story.url}"


def get_hottest(_: deque, __: str, ___: str) -> str:
    hottest_story = api.top_stories(limit=1)[0]
    if hottest_story.text:
        return f"The hottest news is '{hottest_story.title}'! This is the article!\n{hottest_story.text}"
    else:
        return f"Uau! Have you see this news? '{hottest_story.title}' See more in {hottest_story.url}"
