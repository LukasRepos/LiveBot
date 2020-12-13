import json
import re
from typing import Dict, Any

import wikipedia

from Chatty.API.wolframalphaAPI import Wolframalpha

with open("../sandbox/configuration/APIKEYS.json") as f:
    keys = json.load(f)

wolframalpha_API = Wolframalpha(keys["WOLFRAM_ALPHA"])


def search_in_wolframalpha(data: Dict[str, Any]):
    reg = r"for (.+)"
    doc = data["document"]
    match = re.findall(reg, doc)
    subject = match[0]
    return wolframalpha_API.search(subject)


def search_in_wikipedia(data: Dict[str, Any]):
    reg = r"for (.+)"
    doc = data["document"]
    match = re.findall(reg, doc)
    subject = match[0]
    try:
        search_results = wikipedia.search(subject)
        page = wikipedia.page(search_results[0], auto_suggest=False)
        return page.summary
    except wikipedia.DisambiguationError:
        return "Too much results! Narrow down the search query!"


def search_all(data: Dict[str, Any]):
    search_in = [search_in_wolframalpha, search_in_wikipedia]
    name_to_desc = {
        "search_in_wolframalpha": "Wolfram Alpha",
        "search_in_wikipedia": "Wikipedia"
    }

    results = [r(data) for r in search_in]
    msgs = []
    for result, search_func in zip(results, search_in):
        msgs.append(f"From {name_to_desc[search_func.__name__]}:")
        msgs.append(result)

    return "\n".join(msgs)
