from cognitive.cognition import CognitiveFunction

if __name__ == "__main__":
    cognition = CognitiveFunction("./configuration/memoryConfig.xml")
    while True:
        inp = input("> ")

        if inp == "quit":
            break
        elif inp == "##df":
            print(cognition.language.classifier.df)
        else:
            print(cognition.process_language(inp))

    cognition.shutdown()
