import functools
from collections import deque
from functools import partial
from random import choice
from typing import Dict, Union, Callable, List, Any

from Chatty.cognitive.module import ChattyModule
from Chatty.models.tfidf import TfIdf
from Chatty.utilities.tables import table


def base_response(_, data):
    return choice(data)


class LearningModule(ChattyModule):
    def __init__(self, classifier: TfIdf, classifications: List[str], responses: Dict[str, Callable[[Dict[str, Any]], str]]):
        self.classifications = classifications
        self.lang_classifier = classifier
        self.responses = responses

        self.classifier = TfIdf()

        self.classifier.submit_document("That's not right!", "learn")
        self.classifier.submit_document("You can improve on that classification...", "learn")
        self.classifier.submit_document("That classification is wrong!", "learn")

        self.classifier.fit()

        self.is_ready_to_stop = False
        self.is_first_time = False
        self.is_training = False
        self.is_learning_responses = False
        self.previous_doc = ""
        self.current_doc = ""
        self.class_ = ""

        self.new_responses = []

        self.THRESHOLD = 0.8

    def prepare(self):
        self.is_ready_to_stop = False
        self.is_first_time = True

    def process_nlp(self, doc):
        if self.is_first_time:
            self.is_first_time = False
            msg = "Please teach me or type ##quit to end learning!\n"
            msg += "Choose a classification! Or create your own!\n"
            msg += table(list(filter(lambda x: x[0].islower(), self.responses)), 3)
            return msg

        if self.is_learning_responses:
            if doc == "##quit":
                self.responses[self.class_] = functools.partial(base_response, data=self.new_responses)
                self.is_ready_to_stop = True
                return "This was fun!"

            self.new_responses.append(doc)
            return "Nice one! Anymore? Remember, type ##quit to stop learning!"

        if doc == "##quit":
            self.is_ready_to_stop = True
            return "Ok, thats fine"

        self.class_ = doc
        self.lang_classifier.submit_document(self.previous_doc, self.class_)
        self.lang_classifier.fit()

        if doc in self.classifications:
            self.is_ready_to_stop = True
        else:
            self.is_learning_responses = True
            return "Now what should I say? Type ##quit to end learning!"

        return "Learned something new! That was exciting!"

    def pass_to(self):
        return None

    def process_ended(self):
        return self.is_ready_to_stop

    def finalize(self):
        self.is_ready_to_stop = False
        self.is_training = False
        self.is_first_time = False
        self.is_learning_responses = False
        self.previous_doc = ""
        self.current_doc = ""
        self.new_responses = []

    def watch(self, doc):
        if not self.is_training:
            self.previous_doc = self.current_doc
            self.current_doc = doc

        classifer_results = self.classifier.classify_document(doc)
        certainty = classifer_results[0]

        if certainty > self.THRESHOLD:
            self.is_training = True
