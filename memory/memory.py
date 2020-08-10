import json
import random
import xml.etree.ElementTree as ElTree
from functools import partial

import fileSystem.fs as fs
import logger.logger as logger
from history.history import History
from models.tfidf import TfIdf


class Memory:
    def __init__(self, config_file):
        file = ElTree.parse(config_file)
        root = file.getroot()
        file_data = {"responses": {}, "models": {}}
        self.classifier = TfIdf()
        self.learning = False
        self.learning_word = ""
        error = False

        for el in root:
            if el.tag == "resource":
                attr = el.keys()

                if "type" in attr and "inline" in attr and "name" and el.get("type") == "responses":
                    data = []
                    for d in el:
                        data.append(d.text)
                    file_data["responses"][el.get("name")] = partial(random.choice, data)
                elif "type" in attr and "inline" in attr and "class" in attr and el.get("type") == "intents":
                    patterns = []
                    for d in el:
                        patterns.append(d.text)
                    file_data["models"][el.get("name")].append({"patterns": patterns, "classification": el.get("class")})
                elif "type" in attr and "filetype" in attr and "source" in attr and "name" in attr and el.get("type") == "intents":
                    if el.get("filetype") == "json":
                        file_data["models"][el.get("name")] = json.load(fs.getStream(el.get("source")))["docs"]
                    else:
                        logger.error(f"Invalid filetype in config file \"{el.get('filetype')}\"")
                        error = True
                else:
                    logger.error("Invalid config file!" + str(el.keys()))
                    error = True

        if not error:
            for doc in file_data["models"]["__root__"]:
                classification = doc["classification"]
                for pattern in doc["patterns"]:
                    self.classifier.submit_document(pattern, classification)

        self.responses = file_data["responses"]
        self.classifier.fit()

    def get_classifier(self):
        return self.classifier

    def remember(self):
        _class = History.get_most_recent()["classification"]
        prob = History.get_most_recent()["probability"]
        inp = History.get_most_recent()["input"]

        if self.learning:
            if inp in self.responses.keys():
                self.classifier.submit_document(self.learning_word, inp)
                self.classifier.fit()
            self.learning = False
            return "Learned"

        if prob < 0.75:
            self.learning = True
            self.learning_word = inp
            return "I didn't understand, is that a thing of the following? " + str(list(filter(lambda x: x != "None", list(self.responses.keys()))))

        if _class in self.responses:
            return self.responses[_class]()
        else:
            return self.responses["None"]()

    def __repr__(self):
        res = str(self.responses) + "\n" + str(self.classifier)
        return res


if __name__ == "__main__":
    mem = Memory("./memoryConfig.xml")
