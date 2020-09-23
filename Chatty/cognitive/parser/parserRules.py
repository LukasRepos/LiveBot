import importlib
import json
import pathlib
import random
from collections import deque
from functools import partial
from typing import Dict, List, Callable

from Chatty.cognitive.parser.parser import ParserRule
from Chatty.fileSystem.fs import FileSystem
from Chatty.fileSystem.filesystems import add_filesystem, access_fs


class PathRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "source"])
        self.configs = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "path":
            self.configs[attributes["type"]] = attributes["source"]
            fs = FileSystem(access_fs("base").root / pathlib.PurePath(attributes["source"]))
            add_filesystem(attributes["type"], fs)

    def get_configs(self) -> Dict[str, str]:
        return self.configs


class InlineReponsesRule(ParserRule):
    def __init__(self):
        super().__init__(["inline", "type", "name"])
        self.responses = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "resource" and attributes["inline"] == "TRUE" and attributes["type"] == "responses":
            self.responses[attributes["name"]] = lambda hist, doc, reference: partial(random.choice, data)()

    def get_responses(self) -> Dict[str, Callable[[deque, str, str], str]]:
        return self.responses


class ExternalScriptRule(ParserRule):
    def __init__(self):
        super().__init__(["type", "name", "source", "function"])
        self.responses = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "resource" and attributes["type"] == "responses":
            self.responses[attributes["name"]] = [attributes["source"], attributes["function"]]

    def get_responses(self, paths):
        for name, [source, func] in self.responses.items():
            self.responses[name] = getattr(importlib.import_module(source, paths["scriptsModule"]), func)
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