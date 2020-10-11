class ChattyModule:
    def prepare(self):
        raise NotImplementedError("[PREPARE] is an obligatory method to override")

    def process_nlp(self, doc):
        raise NotImplementedError("[PROCESS_NLP] is an obligatory method to override")

    def pass_to(self):
        raise NotImplementedError("[PASS_TO] is an obligatory method to override")

    def process_ended(self):
        raise NotImplementedError("[END_PROCESS] is an obligatory method to override")

    def finalize(self):
        raise NotImplementedError("[FINALIZE] is an obligatory method to override")
