from Chatty.entrypoint import EntryPoint

working_directory = "./sandbox"
configuration_file = "./configuration/memoryConfig.xml"
memory_database = "./configuration/memory.db"
intents_folder = "./configuration/intents"

if __name__ == "__main__":
    chatty = EntryPoint(working_directory, memory_database, configuration_file, intents_folder)
    while True:
        try:
            inp = input("> ")
        except KeyboardInterrupt:
            break

        if inp == "##EXIT##":
            break
        else:
            print(chatty.process_nlp(inp))

    chatty.shutdown()
