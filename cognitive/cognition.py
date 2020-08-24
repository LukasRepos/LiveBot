from cognitive.language.lang import Language
from cognitive.parser.parser import Parser
from logger import logger


class CognitiveFunction:
    def __init__(self, parser_config):
        # initialize parser
        self.memory = Parser(parser_config)

        if self.memory.get_error():
            logger.error("Could not initialize! See error log for more details.")
            return

        # initialize language module
        self.language = Language(self.memory)

    def process_language(self, doc):
        return self.language.read(doc)

    def shutdown(self):
        self.memory.shutdown()
        self.language.shutdown()
