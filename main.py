# region imports
from history.history import History
# endregion
from memory.memory import Memory

mem = Memory("./memory/memoryConfig.xml")

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
