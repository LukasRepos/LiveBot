import os
from collections import deque
from functools import partial
from typing import List, Dict

from tqdm import tqdm

from fileSystem.filesystems import access_fs
from logger import logger
from models.sentrecon import recognize_sentiment
from models.tfidf import TfIdf


class Language:
    def __init__(self, paths: Dict[str, str], responses: Dict[str, partial], intents: Dict[str, List[str]]):
        self.recon_threshold = 0.75
        self.MAX_QUEUE_SIZE = 100

        self.history = deque()
        self.classifier = TfIdf()

        self.responses = responses

        path = paths["classifier"]

        if os.path.isfile(access_fs("config").root / path):
            print("Loading classifier data")
            self.classifier.load(path)
        else:
            for classification, patterns in tqdm(intents.items(), desc="Loading classifier"):
                for pattern in patterns:
                    self.classifier.submit_document(pattern, classification)
            self.classifier.fit()

        self.error = False
        self.learning_mode = False
        self.learning_document = None

    def get_error(self) -> bool:
        return self.error

    def read(self, doc: str) -> str:
        classify_results = self.classifier.classify_document(doc)
        self.history.appendleft({
            "input": doc,
            "probability": classify_results[0],
            "classification": classify_results[1],
            "sentiment": recognize_sentiment(doc)
        })

        if len(self.history) > self.MAX_QUEUE_SIZE:
            self.history.pop()

        if self.learning_mode:
            if doc in self.responses.keys():
                self.classifier.submit_document(self.learning_document, doc)
                self.classifier.fit()
            self.learning_mode = False
            return "Learned a new thing!"

        if classify_results[0] < self.recon_threshold:
            self.learning_mode = True
            self.learning_document = doc
            return f"Is it {classify_results[1]}"

        if classify_results[1] in self.responses:
            return self.responses[classify_results[1]]()
        else:
            logger.warning("Classification not found!")
            return self.responses["None"]()

    def shutdown(self) -> None:
        self.classifier.save("./classifier.csv")
