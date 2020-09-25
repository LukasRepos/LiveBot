from Chatty.cognitive.language.lang import Language
from Chatty.cognitive.parser.parser import Parser
from Chatty.cognitive.parser.parserRules import PathRule, InlineReponsesRule, ExternalScriptRule, ExternalIntentRule, InternalIntentRule

import pathlib

from Chatty.fileSystem.filesystems import add_filesystem
from Chatty.fileSystem.fs import FileSystem
from Chatty.saveState.saves import get_conn

import nest_asyncio


class CognitiveFunction:
    def __init__(self, parser_config: str, str_base_path: str) -> None:
        nest_asyncio.apply()

        base_path = "../" / pathlib.PurePath(str_base_path)
        add_filesystem("base", FileSystem(base_path))
        add_filesystem("config", FileSystem(base_path / pathlib.PurePath(parser_config)))

        # initialize rules
        path_rule = PathRule()

        inline_responses_rule = InlineReponsesRule()
        external_scripts_rule = ExternalScriptRule()

        external_intents_rule = ExternalIntentRule()
        internal_intents_rule = InternalIntentRule()

        # initialize parser
        self.parser = Parser()

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

        self.language_module = Language(responses, intents)

    def process_language(self, doc: str) -> str:
        return self.language_module.read(doc)

    def shutdown(self) -> None:
        self.language_module.shutdown()
        self.parser.shutdown()
        get_conn().shutdown()
