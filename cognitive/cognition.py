from cognitive.language.lang import Language
from cognitive.parser.parser import Parser
from cognitive.parser.parserRules import PathRule, InlineReponsesRule, ExternalScriptRule, ExternalIntentRule, InternalIntentRule

import pathlib

from fileSystem.filesystems import add_filesystem
from fileSystem.fs import FileSystem


class CognitiveFunction:
    def __init__(self, parser_config: str) -> None:
        add_filesystem("config", FileSystem(pathlib.PurePath(parser_config).parent))

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
        self.language_module.shutdown()
        self.parser.shutdown()
