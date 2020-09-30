import os
from collections import deque
from functools import partial
import random
from typing import List, Dict, Callable, Union

from tqdm import tqdm

from Chatty.cognitive.learn.learning import LearnModule
from Chatty.fileSystem.filesystems import try_access_fs, access_fs
from Chatty.logger import logger
from Chatty.models.sentrecon import recognize_sentiment
from Chatty.models.tfidf import TfIdf
from Chatty.saveState.saves import initialize_conn


# default response object for every response given
def base_response(_, __, ___, data):
    return random.choice(data)


class Language:
    def __init__(self, classifier: TfIdf, responses: Dict[str, Union[Callable[[deque, str, str], str], partial]]):
        self.recon_threshold = 0.80
        self.MAX_QUEUE_SIZE = 100
        self.history = deque()
        self.classifier = classifier
        self.responses = responses
        self.error = False
        self.learning_module = LearnModule()

    def get_error(self) -> bool:
        return self.error

    def read(self, doc: str) -> str:
        classify_results = self.classifier.classify_document(doc)
        self.history.appendleft({
            "input": doc,
            "probability": classify_results[0],
            "classification": classify_results[1],
            "sentiment": recognize_sentiment(doc),
            "current_sent_value": ((self.history[0]["sentiment"]["compound"] if len(self.history) > 0 else 0) + recognize_sentiment(doc)["compound"]) / 2
        })
        print("Certainty:", classify_results[0])

        if len(self.history) > self.MAX_QUEUE_SIZE:
            self.history.pop()

        # learning
        if self.learning_module.is_learning():
            response = self.learning_module.learn(doc)
            if done := self.learning_module.done():
                if done[1]:
                    self.responses[done[0]] = partial(base_response, data=done[1])
            return response

        if classify_results[0] < self.recon_threshold:
            self.learning_module.new_round(self.history.copy(), self.classifier, list(self.responses.keys()))
            return self.learning_module.ask()

        if classify_results[1] in self.responses:
            return self.responses[classify_results[1]](self.history, doc, classify_results[2])
        else:
            print("Classification not found!")
            return self.responses["None"](self.history, doc, classify_results[2])
