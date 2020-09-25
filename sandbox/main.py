from Chatty.cognitive.cognition import CognitiveFunction

working_directory = "./sandbox"
configuration_file = "./configuration/memoryConfig.xml"

if __name__ == "__main__":
    cognition = CognitiveFunction(configuration_file, working_directory)
    while True:
        try:
            inp = input("> ")
        except KeyboardInterrupt:
            break

        if inp == "##EXIT##":
            break
        else:
            print(cognition.process_language(inp))

    cognition.shutdown()
