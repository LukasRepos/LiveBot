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
    def __init__(self, intents: Dict[str, Dict[str, Any]], responses: Dict[str, Callable[[Dict[str, Any]], str]]):
        self.classifications = []
        for class_ in intents.keys():
            self.classifications.append(class_)

        self.intents = intents
        self.responses = responses

        self.is_first_time = False
        self.is_receiving_class = False
        self.is_receiving_responses = False
        self.is_receiving_context = False
        self.is_receiving_new_context = False

        self.is_ending = False
        self.skip_creation = False
        self.skip_all = False

        self.class_ = ""
        self.context = ""
        self.new_context = ""
        self.pattern = ""
        self.prev_doc = ""

        self.new_responses = []

    def prepare(self):
        self.is_first_time = True
        self.is_receiving_class = False
        self.is_receiving_responses = False
        self.is_receiving_context = False
        self.is_receiving_new_context = False

        self.is_ending = False
        self.skip_creation = False
        self.skip_all = False

        self.class_ = ""
        self.context = ""
        self.new_context = ""
        self.pattern = ""
        self.prev_doc = ""

        self.new_responses = []

    def process_nlp(self, doc):
        # prints the message for the first time
        if self.is_first_time:
            self.pattern = doc
            self.is_first_time = False
            self.is_receiving_class = True
            return table(self.classifications, 3)

        # receives the class
        if self.is_receiving_class:
            if doc == "##quit":
                self.skip_all = True
                self.is_ending = True
                return "Ok"

            self.is_receiving_class = False
            self.class_ = doc
            if self.class_ not in self.classifications:
                self.is_receiving_responses = True
                self.is_receiving_context = True
                self.is_receiving_new_context = True
                return "Ok, now that I have the classification, I just some more informations... Now I need the context, if you don't know what this is, just type 'GENERAL'"

            self.is_ending = True
            self.skip_creation = True
            return "Nice!"

        # context
        if self.is_receiving_context:
            self.is_receiving_context = False
            self.context = doc
            return f"Ok the context is {self.context}, now what would be the new context? Remember, if you don't know what does this mean just type 'GENERAL'"

        # new context
        if self.is_receiving_new_context:
            self.is_receiving_new_context = False
            self.new_context = doc
            if self.is_receiving_responses:
                return f"Nice, the new context will be {self.new_context}! Now just type the responses!"
            return f"Nice, the new context will be {self.new_context}! And we are done!"

        # receives responses - ENDS PROCESS!!
        if self.is_receiving_responses:
            if doc == "##quit":
                self.is_receiving_responses = False
                self.is_ending = True
                return "Ok those were enough!"

            self.new_responses.append(doc)
            return "Ok thats a nice one! Any more?"

        self.is_ending = True
        return "[ERROR]"

    def pass_to(self):
        pass

    def process_ended(self):
        return self.is_ending

    def finalize(self):
        if self.skip_all:
            return

        if self.skip_creation:
            self.intents[self.class_]["patterns"].append(self.pattern)
        else:
            self.intents[self.class_] = {
                "patterns": [self.pattern],
                "context": self.context,
                "new_context": self.new_context,
            }

            self.responses[self.class_] = functools.partial(base_response, data=self.new_responses)

        self.classifications = []
        for class_ in self.intents.keys():
            self.classifications.append(class_)
