import importlib
import json
import random
from functools import partial
from typing import Dict, List

from cognitive.parser.parser import ParserRule


class PathRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "source"])
        self.configs = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "path":
            self.configs[attributes["type"]] = attributes["source"]

    def get_configs(self) -> Dict[str, str]:
        return self.configs


class InlineReponsesRule(ParserRule):
    def __init__(self):
        super().__init__(["inline", "type", "name"])
        self.responses = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "resource" and attributes["inline"] == "TRUE" and attributes["type"] == "responses":
            self.responses[attributes["name"]] = partial(random.choice, data)

    def get_responses(self) -> Dict[str, partial]:
        return self.responses


class ExternalScriptRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "name", "source"])
        self.responses = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "resource" and attributes["type"] == "responses":
            self.responses[attributes["name"]] = attributes["source"]

    def get_responses(self, paths):
        for name, source in self.responses.items():
            self.responses[name] = importlib.import_module(source, paths["scriptModule"]).response
        return self.responses


class ExternalIntentRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "filetype", "source"])
        self.intents = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "resource" and attributes["type"] == "intents":
            with open(attributes["source"]) as f:
                data = json.load(f)

            for doc in data["docs"]:
                self.intents[doc["classification"]] = doc["patterns"]

    def get_intents(self):
        return self.intents


class InternalIntentRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "inline", "name"])
        self.intents = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "resource" and attributes["inline"] == "TRUE" and attributes["type"] == "intents":
            self.intents[attributes["name"]] = data

    def get_intents(self):
        return self.intents
