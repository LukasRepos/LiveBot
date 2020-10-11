from Chatty.cognitive.NLP.nlpLoader import retrieve_nlp_model
from Chatty.cognitive.NLP.svoExtraction import get_svo_sent
from Chatty.cognitive.module import ChattyModule


class NlpModule(ChattyModule):
    def __init__(self):
        self.tree = []
        self.sents = []

    def watch(self, doc):
        sent = retrieve_nlp_model()(doc)
        self.sents.append(sent)
        self.tree.append(get_svo_sent(sent))

    def prepare(self):
        pass

    def process_nlp(self, doc):
        pass

    def pass_to(self):
        pass

    def process_ended(self):
        pass

    def finalize(self):
        pass
