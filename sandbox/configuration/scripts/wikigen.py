from random import choice
from re import sub
from typing import Dict, Any

import wikipedia

from Chatty.cognitive.language.text_generation import Markov, chain_exists, get_chain, add_chain


def response(data: Dict[str, Any]) -> str:
    reference = data["reference"].lower()
    doc = data["document"].lower()
    if reference in doc:
        subject = doc.split(reference)[1]
    else:
        return "I didn't understand!"

    print(subject)

    if not chain_exists(subject):
        markov = Markov(order=30)
        try:
            corpus = wikipedia.page(subject).content
            corpus = sub(r"={2,3}.*={2,3}", "", corpus)
            corpus = sub(r"\(.*\)", "", corpus)
            corpus = sub(r"\".*\"", "", corpus)
            corpus = sub(r"`.*`", "", corpus)
            corpus = sub(r"{.*}", "", corpus)
            corpus = corpus.replace("\n", "")
            markov.train(corpus)
            add_chain(subject, markov)
            return markov.generate(choice([k for k in markov.chain.keys() if not k[0].islower()]), iterations=1500)
        except Exception as e:
            print(e)
            return "Unknow error );"
    else:
        markov = get_chain(subject)
        msg = markov.generate(choice([k for k in markov.chain.keys() if not k[0].islower()]), iterations=1500)
        return msg
