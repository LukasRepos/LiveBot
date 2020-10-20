import xml.etree.ElementTree as ElTree
from typing import List, Dict, KeysView

from tqdm import tqdm

import Chatty.fileSystem.filesystems as fss


# BASE CLASS FOR A RULE
class ParserRule:
    def __init__(self, requirements: List[str]):
        self.requirements = requirements

    def get_requirements(self) -> List[str]:
        return self.requirements

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> bool:
        pass


class Parser:
    def __init__(self) -> None:
        self.rules = []

    def parse(self) -> None:
        file = ElTree.parse(fss.access_fs("config").root)
        root = file.getroot()

        for el in tqdm(root, desc="Loading configuration file"):
            attrs = el.keys()
            has_found = False
            data = []
            for d in el:
                data.append(d.text)
            for rule in self.rules:
                requirements = rule.get_requirements()
                if self.require(attrs, requirements):
                    has_found = has_found or rule.process_tag(el.tag, el.attrib, data)  # ensures that is True even if not processed

            if not has_found:
                print(f"[ERROR] Parser rule not recognized with tag: '{el.tag}' and attributes: '{el.attrib}'")

    def require(self, attrs: KeysView[str], requirements: List[str]) -> bool:
        if len(attrs) != len(requirements):
            return False

        for req in requirements:
            if req not in attrs:
                return False
        return True

    def add_rule(self, rule: ParserRule) -> None:
        self.rules.append(rule)
