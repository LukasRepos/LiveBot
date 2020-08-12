import os
from collections import deque

from logger import logger
from models.sentrecon import recognize_sentiment
from models.tfidf import TfIdf


class Language:
    def __init__(self, memory):
        self.recon_threshold = 0.75
        self.MAX_QUEUE_SIZE = 100

        self.history = deque()
        self.classifier = TfIdf()
        self.memory = memory

        self.path = self.memory.get_language_module_defs()["classifierPath"]

        if os.path.isfile(self.path):
            self.classifier.load(self.path)
        else:
            docs = self.memory.get_language_memory()
            for doc in docs:
                classification = doc["classification"]
                for pattern in doc["patterns"]:
                    self.classifier.submit_document(pattern, classification)
            self.classifier.fit()

        self.error = False
        self.learning_mode = False
        self.learning_document = None

    def get_error(self):
        return self.error

    def read(self, doc):
        classify_results = self.classifier.classify_document(doc)
        print(classify_results)
        self.history.appendleft({
            "input": doc,
            "probability": classify_results[0],
            "classification": classify_results[1],
            "sentiment": recognize_sentiment(doc)
        })

        if len(self.history) > self.MAX_QUEUE_SIZE:
            self.history.pop()

        if self.learning_mode:
            if doc in self.memory.get_responses().keys():
                self.classifier.submit_document(self.learning_document, doc)
                self.classifier.fit()
            self.learning_mode = False
            return "Learned a new thing!"

        if classify_results[0] < self.recon_threshold:
            self.learning_mode = True
            self.learning_document = doc
            return f"Is it {classify_results[1]}"

        if classify_results[1] in self.memory.get_responses():
            return self.memory.get_responses()[classify_results[1]]()
        else:
            logger.warning("Classification not found!")
            return self.memory.get_responses()["None"]()

    def shutdown(self):
        self.classifier.save("./classifier.csv")
