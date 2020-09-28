from collections import deque
from typing import Dict, Callable, List

from Chatty.cognitive.language.lang import Language
from Chatty.models.tfidf import TfIdf


class CognitiveFunction:
    def __init__(self):
        self.language_module = None

    def load_serialized(self, classifier: TfIdf(), responses: Dict[str, Callable[[deque, str, str], str]]) -> None:
        # initialize modules
        self.language_module = Language(classifier, responses)

    def load_objects(self, classifier: TfIdf(), responses: Dict[str, Callable[[deque, str, str], str]]) -> None:
        # initialize modules
        self.language_module = Language(classifier, responses)

    def process_language(self, doc: str) -> str:
        return self.language_module.read(doc)

    def nlp(self, text: str) -> str:
        return self.language_module.read(text)
