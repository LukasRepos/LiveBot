import os
import pathlib
import pickle

import nest_asyncio
from tqdm import tqdm

from Chatty.cognitive.cognition import CognitiveFunction
from Chatty.fileSystem.filesystems import add_filesystem, access_fs
from Chatty.fileSystem.fs import FileSystem
from Chatty.models.tfidf import TfIdf
from Chatty.parser.parser import Parser
from Chatty.parser.parserRules import PathRule, InlineReponsesRule, ExternalScriptRule, ExternalIntentRule, \
    InternalIntentRule
from Chatty.saveState.saves import initialize_conn, get_conn


class EntryPoint:
    def __init__(self, str_base_path: str, db_path: str, parser_config: str) -> None:
        # solve the asynchronous problem with haxor
        nest_asyncio.apply()

        # creates the cognitiom module
        self.cogito = CognitiveFunction()

        # creates the base path
        base_path = "../" / pathlib.PurePath(str_base_path)

        # generates the remaining paths based on the application base path
        add_filesystem("base", FileSystem(base_path))
        add_filesystem("config", FileSystem(base_path / pathlib.PurePath(parser_config)))
        add_filesystem("database", FileSystem(base_path / pathlib.PurePath(db_path)))

        # check if memory file already exists
        db = access_fs("database")
        if os.path.isfile(db.root):
            # load memory database
            initialize_conn()

            # already exists, load it
            responses_list = get_conn().execute_query("SELECT response, data FROM RESERVED_RESPONSES")
            self.responses = {k: pickle.loads(v) for k, v in responses_list}

            self.classifier = TfIdf()
            self.classifier.load()

            self.cogito.load_serialized(self.classifier, self.responses)
        else:
            # does not exist, load XML file
            # initialize rules
            path_rule = PathRule()

            inline_responses_rule = InlineReponsesRule()
            external_scripts_rule = ExternalScriptRule()

            external_intents_rule = ExternalIntentRule()
            internal_intents_rule = InternalIntentRule()

            # initialize parser
            parser = Parser()

            # add the rules to the parser
            parser.add_rule(path_rule)

            parser.add_rule(inline_responses_rule)
            parser.add_rule(external_scripts_rule)

            parser.add_rule(external_intents_rule)
            parser.add_rule(internal_intents_rule)

            # parse everything
            parser.parse()

            # extract parsed data
            path_configs = path_rule.get_configs()
            self.responses = {**inline_responses_rule.get_responses(), **external_scripts_rule.get_responses(path_configs)}
            intents = {**external_intents_rule.get_intents(), **internal_intents_rule.get_intents()}

            # create a connection to the memory database
            initialize_conn()

            # creates internal tables to store responses
            connection = get_conn()
            connection.execute_query("CREATE TABLE RESERVED_RESPONSES ("
                                     "      response string,"
                                     "      data string"
                                     ")")

            # prime the classifier
            self.classifier = TfIdf()

            for classification, patterns in tqdm(intents.items(), desc="Loading classifier"):
                for pattern in patterns:
                    self.classifier.submit_document(pattern, classification)
            self.classifier.fit()

            self.cogito.load_objects(self.classifier, self.responses)

    def process_nlp(self, text: str) -> str:
        return self.cogito.nlp(text)

    def shutdown(self):
        # saves the classifier data
        self.classifier.save()

        pickle.dump(self.responses["None"], open("../../pickle/testPartials.bin", "wb"))

        # pickles the response data
        for k, v in self.responses.items():
            get_conn().execute_query("INSERT INTO "
                                     "RESERVED_RESPONSES(response, data) "
                                     f"VALUES(?, ?)", str(k), pickle.dumps(v))

        # closes the connection with the db
        get_conn().shutdown()
