import xml.etree.ElementTree as ElTree

from typing import List, Dict, KeysView


class ParserRule:
    def __init__(self, requirements: List[str]):
        self.requirements = requirements

    def get_requirements(self) -> List[str]:
        return self.requirements

    def process_tag(self, tag: str, attributes: Dict[str, str], data: List[str]) -> None:
        pass


class Parser:
    def __init__(self, config_file: str) -> None:
        self.rules = []
        self.config_file = config_file

    def parse(self) -> None:
        file = ElTree.parse(self.config_file)
        root = file.getroot()

        for el in root:
            attrs = el.keys()
            for rule in self.rules:
                requirements = rule.get_requirements()
                data = []
                for d in el:
                    data.append(d.text)
                if self.require(attrs, requirements):
                    rule.process_tag(el.tag, el.attrib, data)

    def require(self, attrs: KeysView[str], requirements: List[str]) -> bool:
        if len(attrs) != len(requirements):
            return False

        for req in requirements:
            if req not in attrs:
                return False
        return True

    def add_rule(self, rule: ParserRule) -> None:
        self.rules.append(rule)

    def shutdown(self) -> None:
        pass
