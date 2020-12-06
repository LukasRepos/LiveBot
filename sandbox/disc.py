import discord
from Chatty.entrypoint import EntryPoint
import json

working_directory = "./sandbox"
configuration_file = "./configuration/memoryConfig.xml"
memory_database = "./configuration/memory.db"
intents_folder = "./configuration/intents"
API_keys = "../sandbox/configuration/APIKEYS.json"

if __name__ == "__main__":
    chatty = EntryPoint(working_directory, memory_database, configuration_file, intents_folder)
    client = discord.Client()


    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return
        if str(message.channel) == "geral":
            msg = chatty.process_nlp(message.content)
            if msg.strip():
                await message.channel.send(msg)

    client.run(json.load(open(API_keys))["DISCORD"])
    chatty.shutdown()
