from collections import deque
from typing import Dict, Callable, List

from Chatty.cognitive.language.lang import LanguageModule
from Chatty.cognitive.learn.learnModule import LearningModule
from Chatty.models.tfidf import TfIdf


class CognitiveFunction:
    def __init__(self):
        self.language_module = None
        self.learning_module = None

    def load_serialized(self, classifications, classifier: TfIdf(), responses: Dict[str, Callable[[deque, str, str], str]]) -> None:
        # initialize modules
        self.language_module = LanguageModule(classifier, responses)
        self.learning_module = LearningModule(classifications, responses)

    def load_objects(self, classifications, classifier: TfIdf(), responses: Dict[str, Callable[[deque, str, str], str]]) -> None:
        # initialize modules
        self.language_module = LanguageModule(classifier, responses)
        self.learning_module = LearningModule(classifications, responses)

    def nlp(self, doc: str) -> str:
        learning_mod_response = self.learning_module.process_nlp(doc)
        learning_mod_is_engaged = self.learning_module.is_learning()

        language_mod_response = self.language_module.process_nlp(doc)
        language_mod_certainty = self.language_module.get_certainty()
        language_mod_threshold = self.language_module.get_threshold()

        if not learning_mod_is_engaged and language_mod_certainty < language_mod_threshold:
            self.learning_module.start_learn_process()

        learning_mod_is_engaged = self.learning_module.is_learning()

        if not learning_mod_is_engaged:
            return language_mod_response
        else:
            return learning_mod_response
