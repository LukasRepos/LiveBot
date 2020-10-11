from typing import Any

import spacy

nlp_model = None


def init_nlp_model():
    global nlp_model
    nlp_model = spacy.load("en_core_web_lg")


def retrieve_model() -> Any:
    if nlp_model is None:
        init_nlp_model()
    return nlp_model
