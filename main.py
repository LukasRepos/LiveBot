# region imports
from cognitive.cognition import CognitiveFunction
from history.history import History
# endregion
from cognitive.memory.memory import Memory

"""
mem = Memory("cognitive/memory/memoryConfig.xml")

while True:
    inp = input("> ")

    if inp == "##quit":
        break
    if inp == "##queue":
        History.print_queue()
        continue

    result = mem.get_classifier().classify_document(inp)
    History.add_entry(result, inp)
    print(mem.remember())
"""

if __name__ == "__main__":
    cognition = CognitiveFunction("./configuration/memoryConfig.xml")
    while True:
        inp = input("> ")

        if inp == "quit":
            break

        print(cognition.process_language(inp))

    cognition.shutdown()
