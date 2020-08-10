import json
import random
import xml.etree.ElementTree as ElTree
from functools import partial

import fileSystem.fs as fs
import logger.logger as logger


class Memory:
    def __init__(self, config_file):
        file = ElTree.parse(config_file)
        root = file.getroot()
        file_data = {"responses": {}, "models": {"language": []}, "modules": {"language": {}}}
        self.learning = False
        self.learning_word = ""
        self.error = False

        for el in root:
            if el.tag == "resource":
                attr = el.keys()

                if "type" in attr and "inline" in attr and "name" and el.get("type") == "responses":
                    data = []
                    for d in el:
                        data.append(d.text)
                    file_data["responses"][el.get("name")] = partial(random.choice, data)
                elif "type" in attr and "source" in attr and el.get("type") == "classifier":
                    file_data["modules"]["language"]["classifierPath"] = el.get("source")
                elif "type" in attr and "inline" in attr and "class" in attr and el.get("type") == "intents":
                    patterns = []
                    for d in el:
                        patterns.append(d.text)
                    file_data["models"][el.get("name")].append({"patterns": patterns, "classification": el.get("class")})
                elif "type" in attr and "filetype" in attr and "source" in attr and "name" in attr and el.get("type") == "intents":
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


if __name__ == "__main__":
    mem = Memory("../../configuration/memoryConfig.xml")
