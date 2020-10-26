from collections import deque
from typing import Dict, Callable, List, Any

from Chatty.cognitive.NLP.nlpModule import NlpModule
from Chatty.cognitive.language.languageModule import LanguageModule
from Chatty.cognitive.learn.learnModule import LearningModule
from Chatty.models.tfidf import TfIdf
from Chatty.utilities.stack import Stack


class CognitiveFunction:
    def __init__(self):
        self.modules = {}

        self.watchers = []

        self.module_stack = Stack()
        self.module_stack.push("language")

    def load(self, intents, classifier: TfIdf(), responses: Dict[str, Callable[[Dict[str, Any]], str]]) -> None:
        # initialize modules
        self.modules["NLP"] = NlpModule()
        self.modules["language"] = LanguageModule(responses, intents, self.modules["NLP"])
        self.modules["learning"] = LearningModule(intents, responses)

        # initialize watchers
        self.watchers.append("NLP")

        self.modules[self.module_stack.peek()].prepare()

    def nlp(self, doc: str) -> str:
        for watcher in self.watchers:
            self.modules[watcher].watch(doc)

        module = self.modules[self.module_stack.peek()]
        response = module.process_nlp(doc)

        if module.process_ended():
            module.finalize()
            self.module_stack.pop()
            self.modules[self.module_stack.peek()].prepare()

        if next_module := module.pass_to():
            self.modules[next_module].prepare()
            response = self.modules[next_module].process_nlp(doc)
            self.module_stack.push(next_module)

            return response

        return response
