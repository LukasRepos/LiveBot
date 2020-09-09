import cProfile
from cognitive.cognition import CognitiveFunction

queries = [
    "Hi there",
    "I need to go...",
    "bye!"
]


def main_function():
    cognition = CognitiveFunction("./configuration/memoryConfig.xml")
    for query in queries:
        cognition.process_language(query)
    cognition.shutdown()


results = cProfile.run("main_function()", "stats.prof")
