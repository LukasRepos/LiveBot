from cognitive.cognition import CognitiveFunction

if __name__ == "__main__":
    cognition = CognitiveFunction("./configuration/memoryConfig.xml")
    while True:
        inp = input("> ")

        if inp == "quit":
            break
        else:
            print(cognition.process_language(inp))

    cognition.shutdown()
