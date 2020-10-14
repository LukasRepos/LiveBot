import random
from typing import Dict, Callable, Any

from Chatty.cognitive.NLP.nlpModule import NlpModule
from Chatty.cognitive.module import ChattyModule
from Chatty.models.tfidf import TfIdf


# default response object for every response given
def base_response(_: Dict[str, Any], data):
    return random.choice(data)


class LanguageModule(ChattyModule):
    def __init__(self, classifier: TfIdf, responses: Dict[str, Callable[[Dict[str, Any]], str]], nlp: NlpModule):
        self.classifier = classifier
        self.responses = responses

        self.ready_to_pass = False
        self.THRESHOLD = 0.8
        self.nlp = nlp

    def prepare(self):
        pass

    def process_nlp(self, doc):
        classifier_results = self.classifier.classify_document(doc)

        certainty = classifier_results[0]
        class_ = classifier_results[1]
        reference = classifier_results[2]

        if certainty > self.THRESHOLD:
            return self.responses[class_]({
                "document": doc,
                "reference": reference,
                "NLP": self.nlp.sents[-1]
            })
        else:
            self.ready_to_pass = True
            return ""

    def pass_to(self):
        msg = "learning" if self.ready_to_pass else None
        self.ready_to_pass = False
        return msg

    def process_ended(self):
        return False

    def finalize(self):
        pass


"""
class LanguageModule:
    def __init__(self, classifier: TfIdf, responses: Dict[str, Union[Callable[[deque, str, str], str], partial]]):
        self.recon_threshold = 0.80
        self.MAX_QUEUE_SIZE = 100
        self.history = deque()
        self.classifier = classifier
        self.responses = responses
        self.error = False
        self.learning_module = LearnModule()
        self.certainty = -inf
        self.ready_to_pass = False

    def get_error(self) -> bool:
        return self.error

    def process_nlp(self, doc: str) -> str:
        classify_results = self.classifier.classify_document(doc)
        self.history.appendleft({
            "input": doc,
            "probability": classify_results[0],
            "classification": classify_results[1],
            "sentiment": recognize_sentiment(doc),
            "current_sent_value": ((self.history[0]["sentiment"]["compound"] if len(self.history) > 0 else 0) + recognize_sentiment(doc)["compound"]) / 2
        })
        # print("Certainty:", self.certainty)

        if len(self.history) > self.MAX_QUEUE_SIZE:
            self.history.pop()

        if classify_results[0] >= self.recon_threshold:
            if classify_results[1] in self.responses:
                return self.responses[classify_results[1]](self.history, doc, classify_results[2])
            else:
                print("Classification not found!")
                return self.responses["None"](self.history, doc, classify_results[2])
        else:
            self.ready_to_pass = True
        return ""

    def end_process(self):
        return False
    
    def pass_to(self):
        return "learning" if self.ready_to_pass else None
"""