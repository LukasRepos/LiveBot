import importlib
import json
import random
from collections import deque
from functools import partial
from pathlib import PurePath
from typing import Dict, List, Callable, Any

from Chatty.fileSystem.filesystems import access_fs
from Chatty.parser.parser import ParserRule


# default response object for every response given
def response(_: Dict[str, Any], data):
    return random.choice(data)


class PathRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "source"])
        self.configs = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> bool:
        if tag == "path":
            self.configs[attributes["type"]] = attributes["source"]
            return True
        return False

    def get_configs(self) -> Dict[str, str]:
        return self.configs


class InlineReponsesRule(ParserRule):
    def __init__(self):
        super().__init__(["inline", "type", "name"])
        self.responses = {}
        self.raw_responses = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> bool:
        if tag == "resource" and attributes["inline"] == "TRUE" and attributes["type"] == "responses":
            self.responses[attributes["name"]] = partial(response, data=data)
            self.raw_responses[attributes["name"]] = data
            return True
        return False

    def get_responses(self) -> Dict[str, Callable[[deque, str, str], str]]:
        return self.responses

    def get_raw_responses(self) -> Dict[str, List[str]]:
        return self.raw_responses


class ExternalScriptRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "name", "source", "function"])
        self.responses = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> bool:
        if tag == "resource" and attributes["type"] == "responses":
            self.responses[attributes["name"]] = [attributes["source"], attributes["function"]]
            return True
        return False

    def get_responses(self, paths: Dict[str, str]) -> Dict[str, Callable[[deque, str, str], str]]:
        for name, [source, func] in self.responses.items():
            self.responses[name] = getattr(importlib.import_module(source, paths["scriptsModule"]), func)
        return self.responses


class ExternalIntentRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "filetype", "source"])
        self.intents = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> bool:
        if tag == "resource" and attributes["type"] == "intents":
            with open(access_fs("intents").root / PurePath(attributes["source"])) as f:
                data = json.load(f)

            for doc in data["docs"]:
                self.intents[doc["classification"]] = {
                    "patterns": doc["patterns"],
                    "new_context": doc["new_context"],
                    "context": doc["context"]
                }
            return True
        return False

    def get_intents(self) -> Dict[str, str]:
        return self.intents


class InternalIntentRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "inline", "name", "context", "new_context"])
        self.intents = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> bool:
        if tag == "resource" and attributes["inline"] == "TRUE" and attributes["type"] == "intents":
            self.intents[attributes["name"]] = {
                "patterns": data,
                "new_context": attributes["new_context"],
                "context": attributes["context"]
            }
            return True
        return False

    def get_intents(self) -> Dict[str, List[str]]:
        return self.intents
