from random import choice
from re import sub
from typing import Union, List
from  nltk.tokenize import word_tokenize
import wikipedia

chains = {}


class Markov:
    def __init__(self, order=1):
        self.chain = {}
        self.order = 1

    def train(self, tokens: List[str]) -> None:
        self.create_chain(tokens)

    def create_chain(self, tokens: List[str]) -> None:
        for i in range(self.order, len(tokens) - 1):
            next_tokens = " ".join(tokens[i + 1:i + self.order + 2])
            current_tokens = " ".join(tokens[i - self.order:i + 1])

            if current_tokens in self.chain:
                self.chain[current_tokens].append(next_tokens)
            else:
                self.chain[current_tokens] = [next_tokens]

    def generate(self, seed: str, iterations=500) -> str:
        res = None
        for t in self.chain.keys():
            if seed in t:
                res = [t]
                break
        if res is None:
            return "=-=-=-=-=( ERROR )=-=-=-=-="

        for _ in range(iterations):
            res.append(choice(self.chain[res[len(res) - 1]]))
        return " ".join(res)


def add_chain(name: str, markov_chain: Markov) -> None:
    chains[name] = markov_chain


def get_chain(name: str) -> Union[Markov, None]:
    return chains[name] if name in chains else None


def chain_exists(name: str) -> bool:
    return name in chains.keys()


if __name__ == "__main__":
    markov = Markov(order=15)
    corpus = wikipedia.page("Alan Turing").content
    corpus = sub(r"={2,3}.*={2,3}", "", corpus)
    corpus = sub(r"\(.*\)", "", corpus)
    corpus = sub(r"\".*\"", "", corpus)
    corpus = sub(r"`.*`", "", corpus)
    corpus = sub(r"{.*}", "", corpus)
    corpus = corpus.replace("\n", "")
    markov.train(word_tokenize(corpus))
    print(markov.generate(choice(list(markov.chain.keys())), iterations=100))
