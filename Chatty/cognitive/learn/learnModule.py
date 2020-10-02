from collections import deque
from functools import partial
from typing import Dict, Union, Callable

from Chatty.models.tfidf import TfIdf


class LearningModule:
    def __init__(self, classifications, responses: Dict[str, Union[Callable[[deque, str, str], str], partial]]):
        self.learning = False
        self.current_document = None
        self.sentence_to_evalutate = None
        self.responses = responses
        self.classes = classifications

        print(self.responses)
        print(self.classes)

    def process_nlp(self, document: str) -> str:
        if document == "learn":
            self.start_learn_process()

        self.current_document = document
        """
        if self.learning:
            print(f"I am learning about {self.sentence_to_evalutate}")
        """
        msg = "Choose a classification! Or create your own!\n"
        msg += "\n".join(filter(lambda x: x[0].islower(), self.responses))
        return msg

    def start_learn_process(self) -> None:
        self.sentence_to_evalutate = self.current_document
        self.learning = True

    def is_learning(self) -> bool:
        return self.learning
