import importlib
import json
import random
from functools import partial
from typing import List, Dict

from cognitive.language.lang import Language
from cognitive.parser.parser import Parser, ParserRule


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
        if tag == "resource" and attributes["type"] == "responses":
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
        super().__init__(["type", "inline", "class"])
        self.intents = {}

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        if tag == "resource" and attributes["type"] == "intents":
            self.intents[attributes["class"]] = data

    def get_intents(self):
        return self.intents



class CognitiveFunction:
    def __init__(self, parser_config: str) -> None:
        # initialize rules
        path_rule = PathRule()

        inline_responses_rule = InlineReponsesRule()
        external_scripts_rule = ExternalScriptRule()

        external_intents_rule = ExternalIntentRule()
        internal_intents_rule = InternalIntentRule()

        # initialize parser
        self.parser = Parser(parser_config)

        # add the rules
        self.parser.add_rule(path_rule)

        self.parser.add_rule(inline_responses_rule)
        self.parser.add_rule(external_scripts_rule)

        self.parser.add_rule(external_intents_rule)
        self.parser.add_rule(internal_intents_rule)

        # parse everything
        self.parser.parse()

        # extract parsed
        path_configs = path_rule.get_configs()
        responses = {**inline_responses_rule.get_responses(), **external_scripts_rule.get_responses(path_configs)}
        intents = {**external_intents_rule.get_intents(), **internal_intents_rule.get_intents()}

        self.language_module = Language(path_configs, responses, intents)

    def process_language(self, doc: str) -> str:
        return self.language_module.read(doc)

    def shutdown(self) -> None:
        self.parser.shutdown()
