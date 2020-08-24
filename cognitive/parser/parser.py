import importlib
import json
import random
import xml.etree.ElementTree as ElTree
from functools import partial

import fileSystem.fs as fs
import logger.logger as logger


def require(attrs, *argv):
    for arg in argv:
        if arg not in attrs:
            return False
    return True


class Parser:
    def __init__(self, config_file):
        file = ElTree.parse(config_file)
        root = file.getroot()
        file_data = {"responses": {}, "models": {"language": []}, "modules": {"language": {}}}
        self.learning = False
        self.learning_word = ""
        self.error = False

        relative_import = ""

        for el in root:
            attr = el.keys()
            if el.tag == "config":
                if require(attr, "type", "source") and el.get("type") == "classifier":
                    file_data["modules"]["language"]["classifierPath"] = el.get("source")
                elif require(attr, "type", "source") and el.get("type") == "scriptModule":
                    relative_import = el.get("source")
            elif el.tag == "resource":
                if require(attr, "type", "inline", "name") and el.get("type") == "responses":
                    if require(attr, "filetype", "source") and el.get("filetype") == "script":
                        file_data["responses"][el.get("name")] = importlib.import_module(el.get("source"), relative_import).response
                    else:
                        data = []
                        for d in el:
                            data.append(d.text)
                        file_data["responses"][el.get("name")] = partial(random.choice, data)
                elif require(attr, "type", "name", "inline", "class") and el.get("type") == "intents":
                    patterns = []
                    for d in el:
                        patterns.append(d.text)
                    file_data["models"][el.get("name")].append(
                        {"patterns": patterns, "classification": el.get("class")})
                elif require(attr, "type", "filetype", "source", "name") and el.get("type") == "intents":
                    if el.get("filetype") == "json":
                        filestream = fs.get_stream(el.get("source"))
                        file_data["models"][el.get("name")].extend(json.load(filestream)["docs"])
                        fs.close_stream(filestream)
                    else:
                        logger.error(f"Invalid filetype in config file \"{el.get('filetype')}\"")
                        self.error = True
                        break
                else:
                    logger.error("Invalid config file!" + str(el.keys()))
                    self.error = True
                    break

        if not self.error:
            self.language_memory = file_data["models"]["language"]
            self.modules = {"language": file_data["modules"]["language"]}
            self.responses = file_data["responses"]

    def get_error(self):
        return self.error

    def get_language_memory(self):
        return self.language_memory

    def get_responses(self):
        return self.responses

    def get_language_module_defs(self):
        return self.modules["language"]

    def shutdown(self):
        pass
