from collections import deque
from typing import Tuple, Union, List

from Chatty.models.tfidf import TfIdf


class LearnModule:
    def __init__(self):
        self.learning = False
        self.doc_to_learn = None
        self.history = None
        self.classifier = None
        self.classes = None
        self.returned = False
        self.new_responses = []
        self.learning_responses = False
        self.classification = ""

    def new_round(self, history: deque, classifier: TfIdf, avail_responses: List[str]):
        self.history = history
        self.learning = True
        self.doc_to_learn = self.history[0]["input"]
        self.classifier = classifier
        self.classes = avail_responses
        self.new_responses = []
        self.returned = False
        self.learning_responses = False
        self.classification = ""

    def learn(self, doc: str) -> str:
        if not self.learning_responses:
            self.classification = doc.replace(" ", "_")
            print(self.doc_to_learn, self.classification)
            self.classifier.submit_document(self.doc_to_learn, self.classification)
            self.classifier.fit()
            self.learning_responses = True
            if self.classification in self.classes:
                self.learning = False
                return "Hey, I learned something new!"
            return "Ok, now what should I respond? (type ##quit) to end learning"

        self.learning_responses = True
        return self.learn_responses(doc)

    def ask(self) -> str:
        msg = "I didn't understand ;( Type in the classification! I have the following classifications as an example!"
        for class_ in self.classes:
            msg += f"\n{class_}"
        return msg

    def is_learning(self) -> bool:
        return self.learning

    def done(self) -> Union[bool, Tuple[str, List[str]]]:
        if not self.learning and not self.returned:
            self.returned = True
            return self.classification, self.new_responses
        return False

    def learn_responses(self, doc: str) -> str:
        if doc.lower() == "##quit":
            self.learning = False
            return "Ok, nice!"

        self.new_responses.append(doc)
        return "Ok, thats a good one! Any more?"
