from collections import deque
from random import choice
from re import sub

import wikipedia
from nltk import word_tokenize

from cognitive.language.text_generation import Markov, chain_exists, get_chain, add_chain


def response(_: deque, doc: str, reference: str) -> str:
    reference = reference.lower()
    doc = doc.lower()
    if reference in doc:
        page = doc.split(reference)[1]
    else:
        return "I didn't understand!"

    if not chain_exists(page):
        markov = Markov(order=15)
        try:
            corpus = wikipedia.page(page).content
            corpus = sub(r"={2,3}.*={2,3}", "", corpus)
            corpus = sub(r"\(.*\)", "", corpus)
            corpus = sub(r"\".*\"", "", corpus)
            corpus = sub(r"`.*`", "", corpus)
            corpus = sub(r"{.*}", "", corpus)
            corpus = corpus.replace("\n", "")
            markov.train(word_tokenize(corpus))
            add_chain(page, markov)
            return markov.generate(choice([k for k in markov.chain.keys() if not k[0].islower()]), iterations=100)
        except:
            return "Unknow error );"
    else:
        markov = get_chain(page)
        return markov.generate(choice([k for k in markov.chain.keys() if not k[0].islower()]), iterations=100)
