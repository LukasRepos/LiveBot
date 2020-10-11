from random import choice
from typing import Union, Dict

chains = {}


class Markov:
    def __init__(self, order=1):
        self.chain = {}
        self.order = order

    def train(self, text: str) -> None:
        self.chain = {}

        for i in range(len(text) - self.order):
            gram = text[i:i + self.order]
            if gram not in self.chain:
                self.chain[gram] = []
            self.chain[gram].append(text[i + self.order])

    def generate(self, seed: str, iterations=500, stopwords=".!?") -> str:
        current_gram = None

        for gram in self.chain.keys():
            if gram.lower().startswith(seed[:self.order].lower()):
                current_gram = gram

        if current_gram is None:
            return "Keyword not found"

        result = current_gram
        for _ in range(iterations):
            current_gram = choice(self.chain[result[-self.order:]])
            result += current_gram
            if current_gram in stopwords:
                break
        return result

    def load_from_chain(self, chain: Dict[str, str]) -> None:
        self.chain = chain


def add_chain(name: str, markov_chain: Markov) -> None:
    chains[name] = markov_chain


def get_chain(name: str) -> Union[Markov, None]:
    return chains[name] if name in chains else None


def chain_exists(name: str) -> bool:
    return name in chains.keys()
