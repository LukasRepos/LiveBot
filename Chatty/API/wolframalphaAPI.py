import wolframalpha


class Wolframalpha:
    def __init__(self, api_key: str):
        self.key = api_key
        self.client = wolframalpha.Client(self.key)

    def search(self, query: str) -> str:
        res = self.client.query(query)
        try:
            return next(res.results).text
        except StopIteration:
            return "Could not find results"
