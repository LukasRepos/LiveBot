from collections import deque

from models.sentrecon import recognize_sentiment

MAX_QUEUE_SIZE = 100

class History:
    history = deque()

    @classmethod
    def add_entry(cls, classify_results, inp):
        cls.history.appendleft({
            "input": inp,
            "probability": classify_results[0],
            "classification": classify_results[1],
            "sentiment": recognize_sentiment(inp)
        })

        if len(cls.history) > MAX_QUEUE_SIZE:
            cls.history.pop()

    @classmethod
    def get_most_recent(cls):
        return cls.history[0]

    @classmethod
    def print_queue(cls):
        print(cls.history.__repr__())
