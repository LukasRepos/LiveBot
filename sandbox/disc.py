import discord
from Chatty.entrypoint import EntryPoint

working_directory = "./sandbox"
configuration_file = "./configuration/memoryConfig.xml"
memory_database = "./configuration/memory.db"
intents_folder = "./configuration/intents"

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

    client.run("NzU4MDQwOTA2MTY2MzA0OTA1.X2pKmw.aP_7LtIOL-NQQNMMkoAgg0fMwsY")
    chatty.shutdown()
